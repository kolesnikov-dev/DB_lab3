CREATE OR REPLACE FUNCTION assignPupilToSubject() RETURNS TRIGGER AS $$
declare
	teacherID bigint;
	subjectID bigint;
BEGIN
  	select id into teacherID from public."Teachers" order by random() limit 1;
	select id into subjectID from public."Subjects" order by random() limit 1;
	insert into public."PupilsSubjects"(pupilsid, subjectsid) values (NEW."Id", subjectID);
	insert into public."TeachersSubjects"(teachersid, subjectsid) values (teacherID, subjectID);
    RETURN NULL;
END
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER new_pupil_arrived
AFTER INSERT ON public."Pupils"
FOR EACH ROW EXECUTE PROCEDURE assignPupilToSubject();