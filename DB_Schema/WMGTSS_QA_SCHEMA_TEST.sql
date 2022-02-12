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
	CHECK ("course_start" < "course_end" OR "course_end" = NULL)
);

CREATE TABLE "users" (
	"user_id" BIGSERIAL PRIMARY KEY,
	"role_id" INTEGER NOT NULL,
	"user_username" VARCHAR(256) NOT NULL UNIQUE,
	"user_password" VARCHAR(256) ,
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
	"course_id" INTEGER NOT NULL,
	"author_id" INTEGER NOT NULL,
	"post_title" VARCHAR(512) NOT NULL,
	"post_description" VARCHAR(2048),
	"post_answer" VARCHAR(2048),
	"post_created" DATE DEFAULT CURRENT_DATE,
	"post_publishable" BOOLEAN NOT NULL,
	"post_published" BOOLEAN DEFAULT FALSE,
	constraint "fk_course_id" foreign key ("course_id") REFERENCES "courses"("course_id"),
	constraint "fk_author_id" foreign key ("author_id") REFERENCES "users"("user_id")
);

CREATE TABLE "comments" (
	"comment_id" BIGSERIAL PRIMARY KEY,
	"post_id" INTEGER NOT NULL,
	"author_id" INTEGER NOT NULL,
	"parent_id" INTEGER DEFAULT NULL,
	"comment_description" VARCHAR(2048) NOT NULL,
	"comment_created" DATE DEFAULT CURRENT_DATE,
	constraint "fk_post_id" foreign key ("post_id") REFERENCES "posts"("post_id"),
	constraint "fk_author_id" foreign key ("author_id") REFERENCES "users"("user_id"),
	constraint "fk_parent_id" foreign key ("parent_id") REFERENCES "comments"("comment_id")
);

GRANT
	SELECT,
	UPDATE,
	INSERT,
	DELETE
ON ALL TABLES IN SCHEMA
	public
TO
	web_client
;

GRANT 
	USAGE,
	SELECT 
ON ALL SEQUENCES IN SCHEMA
	public 
TO 
	web_client
;

-- ROLES

INSERT INTO
	"roles"("role_name", "role_elevated")
VALUES
	('student', FALSE),
	('teacher', TRUE),
	('moderator', TRUE);