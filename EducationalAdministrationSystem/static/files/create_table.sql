USE EducationalSystem;
CREATE TABLE student
{
	id		int		NOT NULL	AUTO_INCREMENT,
	stu_name	char(50)	NOT NULL,
	stu_gender	char(50)	NOT NULL,
	stu_id		char(50)	NOT NULL,
	stu_dept	char(50)	NOT NULL,
	stu_grade	char(50)	NOT NULL,
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE teacher
{
	id		int		NOT NULL	AUTO_INCREMENT,
	tea_name	char(50)	NOT NULL,
	tea_gender	char(50)	NOT NULL,
	tea_id		char(50)	NOT NULL,
	tea_title	char(50)	NOT NULL,
	tea_mobile	char(20)	NULL,
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE eduadmin
{
	id		int		NOT NULL	AUTO_INCREMENT,
	eadmin_name	char(50)	NOT NULL,
	eadmin_gender	char(50)	NOT NULL,
	eadmin_id	char(50)	NOT NULL,
	eadmin_title	char(50)	NOT NULL,
	eadmin_mobile	char(50)	NULL,
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE term
{
	id		int		NOT NULL	AUTO_INCREMENT,
	term_name	char(50)	NOT NULL,
	term_start	date		NOT NULL,
	term_end	date		NOT NULL,
	term_week	int		NOT NULL,
	term_isover	bool		NOT NULL	DEFAULT FALSE,
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE course
{
	id		int		NOT NULL	AUTO_INCREMENT,
	course_name	char(50)	NOT NULL,
	course_credit	int		NOT NULL,
	course_time	char(50)	NOT NULL,
	course_loc	char(50)	NOT NULL,
	course_teamup	int		NOT NULL,
	course_teamdown	int		NOT NULL,
	term_id		int		NOT NULL,
	FOREIGN KEY (term_id) REFERENCES term(id),
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE course_teacher
{
	id		int		NOT NULL	AUTO_INCREMENT,
	course_id	int		NOT NULL,
	tea_id		int		NOT NULL,
	FOREIGN KEY (course_id) REFERENCES course(id),
	FOREIGN KEY (teacher_id) REFERENCES teacher(id),
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE course_student
{
	id		int		NOT NULL	AUTO_INCREMENT,
	course_id	int		NOT NULL,
	stu_id		int		NOT NULL,
	grade		int		NULL,
	FOREIGN KEY (course_id) REFERENCES course(id),
	FOREIGN KEY (stu_id) REFERENCES student(id),
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE resource
{
	id		int		NOT NULL	AUTO_INCREMENT,
	res_name	char(50)	NOT NULL,
	res_path	char(50)	NULL,
	course_id	int		NOT NULL,
	res_virpath	char(50)	NOT NULL,
	FOREIGN KEY (course_id) REFERENCES course(id),
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE assignment
{
	id		int		NOT NULL	AUTO_INCREMENT,
	course_id	int		NOT NULL,
	asn_name	char(50)	NOT NULL,
	asn_req		text		NOT NULL,
	asn_start	datetime	NOT NULL,
	asn_due		datetime	NOT NULL,
	submit_limit	int		NULL,
	asn_weight	float		NULL,
	FOREIGN KEY (course_id) REFERENCES course(id),
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE team
{
	id		int		NOT NULL	AUTO_INCREMENT,
	team_name	char(50)	NOT NULL,
	course_id	int		NOT NULL,
	is_approved	bool		NOT NULL	DEFAULT FALSE,
	reason		text		NULL,
	FOREIGN KEY (course_id) REFERENCES course(id),
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE team_assignment
{
	id		int		NOT NULL	AUTO_INCREMENT,
	team_id		int		NOT NULL,
	asn_id		int		NOT NULL,
	mark		int		NULL,
	comment		text		NULL,
	submit_time	int		NOT NULL	DEFAULT 0,
	FOREIGN KEY (team_id) REFERENCES team(id),
	FOREIGN KEY (asn_id) REFERENCES assignment(id),
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE assignment_resource
{
	id		int		NOT NULL	AUTO_INCREMENT,
	team_asn_id	int		NOT NULL,
	asn_res_path	char(50)	NOT NULL,
	is_corrected	bool		NOT NULL,
	FOREIGN KEY (team_asn_id) REFERENCES team_assignment(id),
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE student_team
{
	id		int		NOT NULL	AUTO_INCREMENT,
	team_id		int		NOT NULL,
	stu_id		int		NOT NULL,
	is_approved	bool		NOT NULL	DEFAULT FALSE,
	FOREIGN KEY (team_id) REFERENCES team(id),
	FOREIGN KEY (stu_id) REFERENCES student(id),
	PRIMARY KEY (id)
} ENGINE = InnoDB

CREATE TABLE student_assignment_grade
{
	id		int		NOT NULL	AUTO_INCREMENT,
	stu_id		int		NOT NULL,
	team_asn_id	int		NOT NULL,
	weight		float		NULL,
	FOREIGN KEY (stu_id) REFERENCES student(id),
	FOREIGN KEY (team_asn_id) REFERENCES team_assignment(id),
	PRIMARY KEY (id)
}
