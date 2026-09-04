-- Seed Initial Users Data

INSERT INTO users (username, email) VALUES
    ('admin_commander', 'commander@echocrew.io'),
    ('dispatcher_01', 'dispatcher1@echocrew.io'),
    ('crew_lead_alpha', 'lead.alpha@echocrew.io'),
    ('crew_lead_bravo', 'lead.bravo@echocrew.io')
ON CONFLICT (username) DO NOTHING;
