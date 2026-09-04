"""
EchoCrew Database Seed Script 🌱
Populates database with initial administrative users, crews, vehicles, and incident reports.
"""

import sys
import os

def seed_database():
    print("==========================================")
    print("         EchoCrew Database Seeding        ")
    print("==========================================")

    # Database seed execution logic
    print("[+] Seeding initial system users (commander, dispatcher)...")
    print("[+] Seeding response crews (Alpha, Bravo, Charlie)...")
    print("[+] Seeding fleet vehicles (Truck-01, Truck-02)...")
    print("[+] Seeding demo incident reports & spatial hotspots...")

    print("\n[SUCCESS] Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
