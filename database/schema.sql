-- ENUM type to choose only between RAM and CPU 
CREATE TYPE resource_type AS ENUM ('CPU', 'RAM');

-- Create Tables
CREATE TABLE "job" (
    -- Columns
    "id" UUID DEFAULT uuid_generate_v4(),
    "start_time" TIMESTAMPTZ NOT NULL,
    "resource" resource_type NOT NULL, 
    "description" TEXT,     

    -- Primary Key
    PRIMARY KEY ("id")
);


CREATE TABLE "hardware_usage"(
    -- Columns
    "id" SERIAL,
    "date_time" TIMESTAMPTZ NOT NULL, 
    "reading" NUMERIC(7,4),
    "job_id" UUID NOT NULL, 

    -- Primary Key
    PRIMARY KEY ("id"),

    -- Constraints
    CONSTRAINT "job_id" FOREIGN KEY ("job_id") 
	    REFERENCES public."job" ("id")
);


CREATE TABLE "outlier"(
    -- Columns
    "id" SERIAL,
    "date_time" TIMESTAMPTZ NOT NULL, 
    "reading" NUMERIC(7,4), 
    "outlier_flag" BOOLEAN DEFAULT TRUE, 
    "job_id" UUID NOT NULL,

    -- Primary Key 
    PRIMARY KEY ("id"),

    -- Constraints 
    CONSTRAINT "job_id" FOREIGN KEY ("job_id") 
	    REFERENCES public."job" ("id")
);


CREATE TABLE "rolling_window"(
    -- Columns
    "id" SERIAL,
    "date_time" TIMESTAMPTZ NOT NULL, 
    "rolling_value" NUMERIC(7,4),  
    "job_id" UUID NOT NULL,

    -- Primary Key 
    PRIMARY KEY ("id"),

    -- Constraints 
    CONSTRAINT "job_id" FOREIGN KEY ("job_id") 
	    REFERENCES public."job" ("id")
);