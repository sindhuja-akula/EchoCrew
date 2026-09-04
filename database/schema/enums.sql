-- Define Custom Enums for EchoCrew System

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('commander', 'dispatcher', 'crew_lead', 'responder');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE task_status AS ENUM ('pending', 'assigned', 'in_progress', 'completed', 'cancelled');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE risk_level AS ENUM ('low', 'medium', 'high', 'critical');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE vehicle_status AS ENUM ('available', 'deployed', 'maintenance', 'offline');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
