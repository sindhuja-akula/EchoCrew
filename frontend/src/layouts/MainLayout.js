import { Navbar } from '../components/Navbar.js';

export function MainLayout(contentHtml) {
  return `
    <div class="layout-main">
      ${Navbar()}
      <main class="container">
        ${contentHtml}
      </main>
    </div>
  `;
}
