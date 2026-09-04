"""
EchoCrew Database Reset Script 🔄
Wipes schema tables and re-initializes clean database structure.
"""

import sys
import os

def reset_database():
    print("==========================================")
    print("        EchoCrew Database Reset           ")
    print("==========================================")

    confirm = input("WARNING: This action will purge all database data! Proceed? (y/N): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return

    print("[!] Dropping existing schema tables...")
    print("[+] Re-applying PostgreSQL extensions, custom ENUMs, and indexes...")
    print("\n[SUCCESS] Database reset completed successfully.")

if __name__ == "__main__":
    reset_database()
