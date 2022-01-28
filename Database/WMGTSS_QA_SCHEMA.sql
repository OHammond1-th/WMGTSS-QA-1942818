CREATE DATABASE "WMGTSS_QA";

CREATE TABLE "roles" (
	"role_id" BIGSERIAL PRIMARY KEY,
	"role_name" VARCHAR(256) NOT NULL,
	"role_elevated" BOOLEAN DEFAULT FALSE
);

CREATE TABLE "courses" (
	"course_id" BIGSERIAL PRIMARY KEY,
	"course_name" VARCHAR(256) NOT NULL,
	"course_start" DATE,
	"course_end" DATE,
	CHECK ("course_start" < "course_end")
);

CREATE TABLE "users" (
	"user_id" BIGSERIAL PRIMARY KEY,
	"role_id" INTEGER NOT NULL,
	"user_fakename" VARCHAR(256) NOT NULL,
	"user_firstname" VARCHAR(256) NOT NULL,
	"user_lastname" VARCHAR(256) NOT NULL,
	"user_dateofbirth" DATE NOT NULL,
	"user_interacted_last" DATE,
	"user_created" DATE DEFAULT CURRENT_DATE,
	constraint "fk_role_id" foreign key ("role_id") REFERENCES "roles"("role_id"),
	CHECK ("user_dateofbirth" < CURRENT_DATE)
);

CREATE TABLE "enrollments" (
	"enrollment_id" BIGSERIAL PRIMARY KEY,
	"course_id" INTEGER NOT NULL,
	"user_id" INTEGER NOT NULL,
	constraint "fk_course_id" foreign key ("course_id") REFERENCES "courses"("course_id"),
	constraint "fk_user_id" foreign key ("user_id") REFERENCES "users"("user_id")
);

CREATE TABLE "posts" (
	"post_id" BIGSERIAL PRIMARY KEY,
	"author_id" INTEGER NOT NULL,
	"post_title" VARCHAR(512) NOT NULL,
	"post_description" VARCHAR(2048) DEFAULT EMPTY,
	"post_answer" VARCHAR(2048),
	"post_created" DATE DEFAULT CURRENT_DATE,
	"post_published" BOOLEAN DEFAULT FALSE,
	constraint "fk_author_id" foreign key ("author_id") REFERENCES "users"("user_id")
);

CREATE TABLE "comments" (
	"comment_id" BIGSERIAL PRIMARY KEY,
	"post_id" INTEGER NOT NULL,
	"author_id" INTEGER NOT NULL,
	"comment_description" VARCHAR(2048) NOT NULL,
	"parent_id" INTEGER DEFAULT NULL,
	"comment_created" DATE DEFAULT CURRENT_DATE,
	constraint "fk_post_id" foreign key ("post_id") REFERENCES "posts"("post_id"),
	constraint "fk_author_id" foreign key ("author_id") REFERENCES "users"("user_id"),
	constraint "fk_parent_id" foreign key ("parent_id") REFERENCES "comments"("comment_id")
);

-- ROLES

INSERT INTO
	"roles"
VALUES
	('Student'),
	('Teacher', TRUE),
	('Moderator', TRUE);