import { renderNavbar } from './src/components/Navbar.js';
import { getHealth } from './src/services/healthService.js';

import { ReportForm } from './src/components/ReportForm.js';
import { ReportsView } from './src/components/ReportsView.js';
import { SupervisorDashboard } from './src/components/SupervisorDashboard.js';
import { WorkOrdersView } from './src/components/WorkOrdersView.js';
import { AssignmentsView } from './src/components/AssignmentsView.js';
import { VerificationView } from './src/components/VerificationView.js';
import { CompensationView } from './src/components/CompensationView.js';
import { CollectionsView } from './src/components/CollectionsView.js';
import { AuditView } from './src/components/AuditView.js';
import { WorkerView } from './src/components/WorkerView.js';
import { IntelligentVerificationView } from './src/components/IntelligentVerificationView.js';
import { WeighmentView } from './src/components/WeighmentView.js';
import { DisposalView } from './src/components/DisposalView.js';

class Application {
  constructor() {
    this.currentRole = localStorage.getItem('cleanloop_user_role') || 'citizen';
    this.healthStatus = null;
    this.activeComponent = null;

    this.init();
  }

  async init() {
    this.setupEventListeners();
    await this.checkHealth();
    this.handleRoute();

    // Periodic health check every 30 seconds
    setInterval(() => this.checkHealth(), 30000);
  }

  setupEventListeners() {
    window.addEventListener('hashchange', () => this.handleRoute());
    window.addEventListener('role-change', (e) => {
      this.currentRole = e.detail;
      localStorage.setItem('cleanloop_user_role', this.currentRole);

      // Default route per role
      if (this.currentRole === 'citizen') location.hash = '#report';
      else if (this.currentRole === 'supervisor') location.hash = '#dashboard';
      else if (this.currentRole === 'worker') location.hash = '#worker';
    });
  }

  async checkHealth() {
    try {
      this.healthStatus = await getHealth();
    } catch (err) {
      this.healthStatus = { status: 'offline' };
    }
    this.updateNavbar();
  }

  updateNavbar() {
    const navContainer = document.getElementById('navbar-container');
    if (navContainer) {
      navContainer.innerHTML = renderNavbar(location.hash || '#report', this.currentRole, this.healthStatus);
    }
  }

  handleRoute() {
    const hash = location.hash || (this.currentRole === 'citizen' ? '#report' : this.currentRole === 'supervisor' ? '#dashboard' : '#worker');
    this.updateNavbar();

    const pageContainer = 'page-container';

    if (hash === '#report') {
      this.activeComponent = new ReportForm(pageContainer);
      this.activeComponent.render();
    } else if (hash === '#my-reports' || hash === '#reports') {
      this.activeComponent = new ReportsView(pageContainer);
      this.activeComponent.loadData();
    } else if (hash === '#dashboard') {
      this.activeComponent = new SupervisorDashboard(pageContainer);
      this.activeComponent.loadData();
    } else if (hash === '#work-orders') {
      this.activeComponent = new WorkOrdersView(pageContainer);
      this.activeComponent.loadData();
    } else if (hash === '#assignments') {
      this.activeComponent = new AssignmentsView(pageContainer);
      this.activeComponent.loadData();
    } else if (hash === '#verifications') {
      this.activeComponent = new VerificationView(pageContainer);
      this.activeComponent.loadData();
    } else if (hash === '#compensations') {
      this.activeComponent = new CompensationView(pageContainer);
      this.activeComponent.loadData();
    } else if (hash === '#collections') {
      this.activeComponent = new CollectionsView(pageContainer);
      this.activeComponent.loadData();
    } else if (hash === '#ai-verification') {
      this.activeComponent = new IntelligentVerificationView(pageContainer);
      this.activeComponent.render();
    } else if (hash === '#weighments') {
      this.activeComponent = new WeighmentView(pageContainer);
      this.activeComponent.render();
    } else if (hash === '#disposal') {
      this.activeComponent = new DisposalView(pageContainer);
      this.activeComponent.render();
    } else if (hash === '#audit') {
      this.activeComponent = new AuditView(pageContainer);
      this.activeComponent.loadData();
    } else if (hash === '#worker') {
      this.activeComponent = new WorkerView(pageContainer);
      this.activeComponent.loadData();
    } else {
      location.hash = '#report';
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.app = new Application();
});
