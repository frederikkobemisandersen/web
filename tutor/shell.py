# coding: utf-8

from .models import *

# Useful routines for the Django shell.

# Given a bunch of student numbers, translate them to known full names.
def translate_student_numbers(*args):
    def translate(number):
        try:
            prof = TutorProfile.objects.get(studentnumber=number)
            return unicode(number)+u": "+prof.get_full_name()
        except TutorProfile.DoesNotExist:
            return unicode(number)+u" unknown"
    return [translate(number) for number in args]

# Given a tutor group handle and a bunch of student numbers, add tutors to the
# given group.
def add_to_group(handle, *students):
    try:
        group = TutorGroup.objects.get(handle=handle)
    except TutorGroup.DoesNotExist:
        return 'Tutor group does not exist'
    errors = []
    ok = []
    from mftutor.settings import YEAR
    for student in students:
        try:
            tu = Tutor.objects.get(profile__studentnumber=student, year=YEAR)
            tu.groups.add(group)
            ok.append(str(student))
        except Tutor.DoesNotExist:
            errors.append(str(student)+" was not found")

    return {'errors': errors, 'ok': ok}

# Given a tutor group handle and a student number, make the tutor the group
# leader.
def group_leader(handle, studentnumber):
    try:
        group = TutorGroup.objects.get(handle=handle)
    except TutorGroup.DoesNotExist:
        return 'Tutor group does not exist'

    from mftutor.settings import YEAR

    try:
        gl = TutorGroupLeader.objects.get(group=group, year=YEAR)
        return u"Group already has leader "+unicode(gl.tutor)
    except TutorGroupLeader.DoesNotExist:
        pass

    try:
        tutor = Tutor.objects.get(profile__studentnumber=studentnumber, year=YEAR)
    except Tutor.DoesNotExist:
        return str(student)+" was not found"

    TutorGroupLeader(group=group, tutor=tutor, year=YEAR).save()
    return u"OK "+unicode(tutor)

# Enter a read-eval-print loop in which you may change the email addresses of
# tutors.
def read_emails_loop():
    from mftutor.settings import YEAR
    from activation.models import ProfileActivation
    from sys import stdin
    while True:
        print 'studentnumber> ',
        studentnumber = stdin.readline().strip()
        if not studentnumber:
            print 'Bye'
            break
        try:
            prof = TutorProfile.objects.get(studentnumber=studentnumber)
        except TutorProfile.DoesNotExist:
            print 'Not found'
            continue
        print prof
        print 'Groups:', u', '.join(tg.name for tg in TutorGroup.objects.filter(tutor__profile=prof, tutor__year__exact=YEAR).order_by('-visible', 'name'))
        try:
            act = ProfileActivation.objects.get(profile=prof)
        except ProfileActivation.DoesNotExist:
            print 'No profile activation'
            continue
        print act.email
        print 'email> ',
        email = stdin.readline().strip()
        if not email:
            print 'No change'
            continue
        act.email = email
        act.save()
        print 'Saved'
