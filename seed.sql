-- Sample data. Run AFTER schema.sql.
USE job_tracker;

INSERT INTO companies (company_name, industry, website, city, state, notes) VALUES
('TechCorp',          'Software',      'https://www.techcorp.example',   'Austin',        'TX', 'Fast-growing SaaS company. Great benefits.'),
('DataCo',            'Analytics',     'https://www.dataco.example',     'Chicago',       'IL', 'Data consulting firm with remote options.'),
('CloudNine Systems', 'Cloud Hosting', 'https://www.cloudnine.example',  'Seattle',       'WA', NULL),
('BrightPath Health', 'Healthcare IT', 'https://www.brightpath.example', 'Miami',         'FL', 'Hospital software. Met recruiter at career fair.'),
('Pixel Forge',       'Web Design',    'https://www.pixelforge.example', 'New York',      'NY', 'Small agency, mostly front-end work.');

INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements) VALUES
(1, 'Software Developer',        'Full-time',  70000, 90000, 'https://www.techcorp.example/careers/101',  '2026-10-01', JSON_ARRAY('Python', 'SQL', 'Flask')),
(2, 'Data Analyst',              'Full-time',  60000, 75000, 'https://www.dataco.example/jobs/22',        '2026-10-05', JSON_ARRAY('Python', 'SQL', 'Tableau')),
(3, 'Cloud Support Intern',      'Internship', 35000, 42000, 'https://www.cloudnine.example/intern',      '2026-09-20', JSON_ARRAY('Linux', 'AWS', 'Networking', 'Python')),
(4, 'Junior Web Developer',      'Full-time',  55000, 68000, 'https://www.brightpath.example/jobs/7',     '2026-10-12', JSON_ARRAY('HTML', 'CSS', 'JavaScript', 'SQL')),
(5, 'Front-End Developer',       'Contract',   45000, 60000, 'https://www.pixelforge.example/work/fe',    '2026-10-15', JSON_ARRAY('HTML', 'CSS', 'JavaScript', 'React')),
(1, 'IT Help Desk Technician',   'Part-time',  30000, 38000, 'https://www.techcorp.example/careers/155',  '2026-10-18', JSON_ARRAY('Windows', 'Active Directory', 'Customer Service')),
(2, 'Database Administrator',    'Full-time',  72000, 95000, NULL,                                         '2026-10-22', JSON_ARRAY('MySQL', 'SQL', 'Linux', 'Backup and Recovery'));

INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data) VALUES
(1, '2026-10-03', 'Interview', 'v2-backend',  TRUE,
    JSON_OBJECT('date', '2026-12-02', 'time', '10:00', 'type', 'Video', 'interviewer', 'Maria Lopez', 'notes', 'Prepare Flask project demo.')),
(2, '2026-10-07', 'Screening', 'v1-data',     FALSE, NULL),
(3, '2026-09-25', 'Rejected',  'v1-general',  TRUE,  NULL),
(4, '2026-10-14', 'Applied',   'v2-frontend', TRUE,  NULL),
(5, '2026-10-16', 'Offer',     'v2-frontend', FALSE,
    JSON_OBJECT('date', '2026-10-28', 'time', '14:30', 'type', 'In-person', 'interviewer', 'Sam Patel', 'notes', 'Offer received. Reply by Nov 30.')),
(7, '2026-10-24', 'Interview', 'v2-backend',  TRUE,
    JSON_OBJECT('date', '2026-12-10', 'time', '09:00', 'type', 'Technical', 'interviewer', 'Dana Kim', 'notes', 'SQL query challenge.'));

INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes) VALUES
(1, 'Maria Lopez',   'Engineering Manager',   'maria.lopez@techcorp.example',  '512-555-0141', 'https://www.linkedin.com/in/example-maria', 'Hiring manager for Software Developer.'),
(1, 'James Carter',  'Technical Recruiter',   'james.carter@techcorp.example', '512-555-0178', NULL, NULL),
(2, 'Dana Kim',      'Senior Data Engineer',  'dana.kim@dataco.example',       '312-555-0122', 'https://www.linkedin.com/in/example-dana', 'Referred me to the DBA role.'),
(4, 'Alex Rivera',   'HR Coordinator',        'alex.rivera@brightpath.example','305-555-0190', NULL, 'Met at the campus career fair.'),
(5, 'Sam Patel',     'Creative Director',     'sam@pixelforge.example',        '212-555-0166', NULL, NULL);
