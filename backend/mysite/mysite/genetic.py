import copy
import numpy as np

from db.models import User, Student, Teacher, Admin, Course, Course_constraint, Classroom, Course_table
from algorithm.score import schedule_score

class MyCourse:
    def __init__(self, course) -> None:
        self.course_id = course.course_id
        self.course_name = course.course_name
        self.course_max_capacity = course.course_max_capacity
        self.course_introduction = course.course_introduction
        self.course_hour = course.course_hour
        if self.course_hour == 64:
            self.weeks = 16
            self.num_per_weeks = (2, 2)
        else:
            self.weeks = self.course_hour // 2
            self.num_per_weeks = (2)
        self.course_type = course.course_type
        self.course_score = course.course_score
        self.course_teacher = [t.teacher_id for t in Course.course_teacher.through.objects.filter(course_id=self.course_id)] # list for teacher_id
        self.course_time = [] # list for MyTime
        self.course_classroom = None # list for classroom_id
        self.course_student = []
        self.course_constraint = MyCourseConstraint(self)

class MyClassroom:
    def __init__(self, classroom=None, classroom_id=None, classroom_name='None', classroom_capacity=100, classroom_place=(1, 2, 3)):
        if classroom != None:
            self.classroom_id = classroom.classroom_id
            self.classroom_name = classroom.classroom_name
            self.classroom_capacity = classroom.classroom_capacity
            self.classroom_place = classroom.classroom_place
        else:
            self.classroom_id = classroom_id
            self.classroom_name = classroom_name
            self.classroom_capacity = classroom_capacity
            self.classroom_place = classroom_place

class MyCourseConstraint:
    def __init__(self, course):
        try:
            course_constraint = Course_constraint.objects.get(course.course_id)
        except:
            course_constraint = None
        self.course_id = course.course_id
        self.course_continue = course_constraint.course_continue if course_constraint != None else True
        self.course_is_odd_week = course_constraint.course_is_odd_week if course_constraint != None else False
        self.course_smallest_day_number = course_constraint.course_smallest_day_number if course_constraint != None else -1
        self.course_biggest_day_number = course_constraint.course_biggest_day_number if course_constraint != None else -1
        self.max_course_room_ratio = course_constraint.max_course_room_ratio if course_constraint != None else -1

class MyTime:
    def __init__(self, semester=None, week=None, day=None, class_num=None) -> None:
        self.semester = semester
        self.week = week
        self.day = day
        self.class_num = class_num

    def __repr__(self) -> str:        
        return '-'.join([self.semester, str(self.week), str(self.day), str(self.class_num)])
    
    def class_num_for_semester(self):
        return (self.week - 1) * 7 * 12 + (self.day - 1) * 12 + self.class_num

    def __lt__(self, obj):
        return self.class_num_for_semester() < obj.class_num_for_semester()

    def __sub__(self, obj):
        return self.class_num_for_semester() - obj.class_num_for_semester()

def rand_classroom(course, roomRange=1):
    res = MyClassroom(classroom_id=np.random.randint(1, roomRange+1))
    return res

def rand_time(course, semester_range='2021-1', num=1):
    course.week_range, course.day_range, course.class_num_range = (1, 18), (1, 7), (1, 14)
    week_range, day_range, class_num_range = course.week_range, course.day_range, course.class_num_range
    if num == 1:
        res = MyTime()
        res.semester = semester_range
        res.week = np.random.randint(week_range[0], week_range[1] + 1, 1)[0]
        res.day = np.random.randint(day_range[0], day_range[1] + 1, 1)[0]
        res.class_num = np.random.randint(class_num_range[0], class_num_range[1] + 1, 1)[0]
    else:
        res = []
        st_week = np.random.randint(week_range[0], week_range[1] - course.weeks, 1)[0]

        for num_per_week in course.num_per_weeks:
            st_class_num = np.random.choice([x for x in range(class_num_range[0], class_num_range[1] + 1) \
                if x + num_per_week - 1 <= 5 \
                    or (x >= 11 and x + num_per_week - 1 <= 14) \
                    or (x >= 6 and x + num_per_week - 1 <= 10)])
            day = np.random.randint(day_range[0], day_range[1] + 1, 1)[0]
            for week in range(st_week, st_week + course.weeks):
                for class_num in range(st_class_num, st_class_num + num_per_week):
                    res.append(MyTime(semester_range, week, day, class_num))

    return res

class GeneticOptimize:
    def __init__(self, popsize=64, mutprob=0.3, elite=8, maxiter=100):
        # 种群的规模（0-100）
        self.popsize = popsize
        # 变异概率
        self.mutprob = mutprob
        # 精英个数
        self.elite = elite
        # 进化代数（100-500）
        self.maxiter = maxiter
        
    #随机初始化不同的种群
    def init_population(self, courses, roomRange):
        self.population = []
        for _ in range(self.popsize):
            entity = []
            for course in courses:
                course.course_time = sorted(rand_time(course, num=course.course_hour))
                course.course_classroom = rand_classroom(course)
                entity.append(copy.deepcopy(course))
            self.population.append(entity)
            
    #变异
    def mutate(self, eiltePopulation, roomRange):
        #选择变异的个数
        e = np.random.randint(0, self.elite, 1)[0]
        ep = copy.deepcopy(eiltePopulation[e])
        for p in ep:
            pos = np.random.randint(0, 5, 1)[0]
            if pos == 0: # classroom
                p.course_classroom = rand_classroom(p)
            else:
                _time = rand_time(p, num=p.course_hour)
                if pos == 1: # week
                    for i in range(len(p.course_time)):
                        p.course_time[i].week = _time[i].week
                elif pos == 2: # day
                    for i in range(len(p.course_time)):
                        p.course_time[i].day = _time[i].day
                elif pos == 3: # class_num
                    for i in range(len(p.course_time)):
                        p.course_time[i].class_num = _time[i].class_num
                else:
                    for i in range(len(p.course_time)):
                        p.course_time[i] = _time[i]
                p.course_time = sorted(p.course_time)
        return ep

    def crossover(self, eiltePopulation):
        e1 = np.random.randint(0, self.elite, 1)[0]
        e2 = np.random.randint(0, self.elite, 1)[0]
        ep1 = copy.deepcopy(eiltePopulation[e1])
        ep2 = eiltePopulation[e2]
        pos = np.random.randint(0, 4, 1)[0]
        for p1, p2 in zip(ep1, ep2):
            if pos == 0:
                p1.course_classroom = p2.course_classroom
            else:
                if pos == 1: # week
                    for i in range(len(p1.course_time)):
                        p1.course_time[i].week = p2.course_time[i].week
                elif pos == 2: # day
                    for i in range(len(p1.course_time)):
                        p1.course_time[i].day = p2.course_time[i].day
                elif pos == 3: # class_num
                    for i in range(len(p1.course_time)):
                        p1.course_time[i].class_num = p2.course_time[i].class_num
                p1.course_time = sorted(p1.course_time)
        return ep1

    def evolution(self, courses, roomRange=100):
        courses = [MyCourse(course) for course in courses]
        bestScore = 0
        bestcourses = None
        self.init_population(courses, roomRange)
        for i in range(self.maxiter):
            eliteIndex, bestScore = schedule_score(self.population, self.elite)
            print('Iter: {} | conflict: {}'.format(i + 1, bestScore))
            bestcourses = self.population[eliteIndex[0]]
            if bestScore == 0:
                break
            newPopulation = [self.population[index] for index in eliteIndex]
            while len(newPopulation) < self.popsize:
                if np.random.rand() < self.mutprob:
                    newp = self.mutate(newPopulation, roomRange)
                else:
                    newp = self.crossover(newPopulation)
                newPopulation.append(newp)
            self.population = newPopulation
        return bestcourses
