import os
import json
import copy
import numpy as np
import time

from db.models import User, Student, Teacher, Admin, Course, Course_constraint, Classroom, Course_table
from algorithm.score import schedule_score

class MyCourse:
    def __init__(self, course) -> None:
        self.course_id = course.course_id
        self.course_name = course.course_name
        self.course_max_capacity = course.course_max_capacity
        self.course_introduction = course.course_introduction
        self.course_hour = course.course_hour
        if self.course_hour % 3 == 0:
            self.weeks = self.course_hour // 3
            self.num_per_weeks = (3)
        elif self.course_hour % 2 == 0:
            self.weeks = self.course_hour // 2
            self.num_per_weeks = (2)
        else:
            self.weeks = self.course_hour // 1
            self.num_per_weeks = (1)
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
    
    def __repr__(self) -> str:
        return '-'.join(list(map(str, [self.classroom_id, self.classroom_name, self.classroom_capacity, self.classroom_place])))

class MyCourseConstraint:
    def __init__(self, course):
        try:
            course_constraint = Course_constraint.objects.get(course.course_id)
        except:
            course_constraint = None
        self.course_id = course.course_id
        self.course_continue = course_constraint.course_continue if course_constraint != None else True
        self.course_is_odd_week = course_constraint.course_is_odd_week if course_constraint != None else False
        #每周最大/小排课天数
        self.course_smallest_day_number = course_constraint.course_smallest_day_number if course_constraint != None else -1
        self.course_biggest_day_number = course_constraint.course_biggest_day_number if course_constraint != None else -1
        #课程容量和教室容量的比例范围
        self.max_course_room_ratio = course_constraint.max_course_room_ratio if course_constraint != None else -1
        #每天最小/大上课节数
        self.course_smallest_sections = course_constraint.course_smallest_sections if course_constraint!=None else -1
        self.course_biggest_sections = course_constraint.course_biggest_sections if course_constraint!=None else -1
        # TODO 数据库这个类型是str 得处理一下
        self.course_no_sections = course_constraint.course_no_sections if course_constraint!=None else []
        # 是否可在周末上班
        self.course_can_weekends = course_constraint.course_can_weekends if course_constraint!=None else False

class MyTime:
    def __init__(self, semester=None, week=None, day=None, class_num=None) -> None:
        self.semester = semester
        self.week = week
        self.day = day
        self.class_num = class_num

    def __repr__(self) -> str:
        return '-'.join([self.semester, str(self.week), str(self.day), str(self.class_num)])

    def class_num_for_semester(self):
        return self.week * 10000 + self.day * 100 + self.class_num
    
    def __cmp__(self,other):
        if self.week==other.week and self.day==other.day:
            return self.class_num<other.class_num
        elif self.week == other.week:
            return self.day<other.day
        else:
            return self.week<other.week


    def __lt__(self, obj):
        return self.class_num_for_semester() < obj.class_num_for_semester()

    def __sub__(self, obj):
        return self.class_num_for_semester() - obj.class_num_for_semester()

def rand_classroom(course, classrooms):
    ok_classrooms = [classroom for classroom in classrooms if classroom.classroom_capacity >= course.course_max_capacity]
    res = np.random.choice(ok_classrooms)
    return res

def rand_time(course, semester_range='2021-1', num=-1):
    course.week_range, course.day_range, course.class_num_range = (1, 18), (1, 7), (1, 14)
    week_range, day_range, class_num_range = course.week_range, course.day_range, course.class_num_range
    if num == -1:
        res = MyTime()
        res.semester = semester_range
        res.week = np.random.randint(week_range[0], week_range[1] + 1, 1)[0]
        res.day = np.random.randint(day_range[0], day_range[1] + 1, 1)[0]
        res.class_num = np.random.randint(class_num_range[0], class_num_range[1] + 1, 1)[0]
    else:
        res = []
        st_week = np.random.randint(week_range[0], week_range[1] - course.weeks, 1)[0]
        if not isinstance(course.num_per_weeks, list):
            course.num_per_weeks = [course.num_per_weeks]
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
    def __init__(self, popsize=32, mutprob=0.3, elite=8, maxiter=100):
        # 种群的规模（0-100）
        self.popsize = popsize
        # 变异概率
        self.mutprob = mutprob
        # 精英个数
        self.elite = elite
        # 进化代数（100-500）
        self.maxiter = maxiter
        
    #随机初始化不同的种群
    def init_population(self, courses, classrooms):
        self.population = []
        for _ in range(self.popsize):
            entity = []
            for course in courses:
                tmp = rand_time(course, num=course.course_hour)
                course.course_time = sorted(tmp)
                course.course_classroom = rand_classroom(course, classrooms)
                entity.append(copy.deepcopy(course))
            self.population.append(entity)
            
    #变异
    def mutate(self, eiltePopulation, classrooms):
        #选择变异的个数
        e = np.random.randint(0, self.elite, 1)[0]
        ep = copy.deepcopy(eiltePopulation[e])
        for p in ep:
            pos = np.random.randint(0, 5, 1)[0]
            if pos == 0: # classroom
                p.course_classroom = rand_classroom(p, classrooms)
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
                elif pos == 4:
                    for i in range(len(p.course_time)):
                        p.course_time[i] = _time[i]
                p.course_time = sorted(p.course_time)
        return ep
    
    def mutate3(self, eiltePopulation, classrooms):
        #选择变异的个数
        e = np.random.randint(0, self.elite, 1)[0]
        ep = copy.deepcopy(eiltePopulation[e])
        permutation = [i for i in range(len(ep))]
        np.random.shuffle(permutation)
        for pid in permutation[:np.random.choice(range(len(ep)//2))+1]:
        # for p in ep[:np.random.choice(range(len(ep)//2))+1]:
            pos = np.random.randint(0, 5, 1)[0]
            if pos == 0: # classroom
                ep[pid].course_classroom = rand_classroom(ep[pid], classrooms)
            else:
                _time = rand_time(ep[pid], num=ep[pid].course_hour)
                if pos == 1: # week
                    for i in range(len(ep[pid].course_time)):
                        ep[pid].course_time[i].week = _time[i].week
                elif pos == 2: # day
                    for i in range(len(ep[pid].course_time)):
                        ep[pid].course_time[i].day = _time[i].day
                elif pos == 3: # class_num
                    for i in range(len(ep[pid].course_time)):
                        ep[pid].course_time[i].class_num = _time[i].class_num
                elif pos == 4:
                    for i in range(len(ep[pid].course_time)):
                        ep[pid].course_time[i] = _time[i]
                ep[pid].course_time = sorted(ep[pid].course_time)
        return ep

    #变异2
    def mutate2(self, eiltePopulation, classrooms):
        #选择变异的个数
        e = np.random.randint(0, self.elite, 1)[0]
        ep = copy.deepcopy(eiltePopulation[e])
        import collections
        mp = collections.defaultdict(lambda: 0)
        permutation = [i for i in range(len(ep))]
        np.random.shuffle(permutation)
        for i in permutation:
            for _ in range(5):
                confict = 0
                for time in ep[i].course_time:
                    confict += mp['%s-%s' % (time, ep[i].course_classroom)]
                    for teacher_id in ep[i].course_teacher:
                        confict += mp['%s-%s' % (time, teacher_id)]
                if confict == 0:
                    break
                if np.random.randint(0, 2, 1)[0] == 0:
                    ep[i].course_classroom = rand_classroom(ep[i], classrooms)
                else:
                    ep[i].course_time = rand_time(ep[i], num=ep[i].course_hour)
           
            for time in ep[i].course_time:
                mp['%s-%s' % (time, ep[i].course_classroom)] += 1
                for teacher_id in ep[i].course_teacher:
                    mp['%s-%s' % (time, teacher_id)] += 1

        return ep

    def crossover(self, eiltePopulation):
        e1 = np.random.randint(0, self.elite, 1)[0]
        e2 = np.random.randint(0, self.elite, 1)[0]
        ep1 = copy.deepcopy(eiltePopulation[e1])
        ep2 = eiltePopulation[e2]
        _len = len(ep1)
        if np.random.randint(0, 2, 1)[0] == 1:
            _len = np.random.choice(range(len(ep1)//2))+1
        pos = np.random.randint(0, 4, 1)[0]
        for p1, p2 in zip(ep1[:_len], ep2[:_len]):
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

    def evolution(self, courses, classrooms):
        save_path = os.path.join('results', '%s.json' % time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
        print(save_path)
        print('[evolution]')
        courses = [MyCourse(course) for course in courses]
        print('init courses ok!')
        classrooms = [MyClassroom(classroom) for classroom in classrooms]
        print('init classrooms ok!')
        bestScore = 0
        bestcourses = None
        timestamp = time.time()
        self.init_population(courses, classrooms)
        print("init_population time: {}s".format(round(time.time()-timestamp)))
        for i in range(self.maxiter):
            timestamp = time.time()
            eliteIndex, bestScore, hard, soft = schedule_score(self.population, self.elite)
            print('Iter: {} | loss: {}, hard: {}, soft: {}, time: {}s'.format(i + 1, bestScore, hard, soft, round(time.time()-timestamp)))
            bestcourses = self.population[eliteIndex[0]]
            if bestScore == 0:
                break
            newPopulation = [self.population[index] for index in eliteIndex]
            while len(newPopulation) < self.popsize:
                if hard > 0:
                    newp = self.mutate2(newPopulation, classrooms)
                elif np.random.rand() < self.mutprob:
                    newp = self.mutate3(newPopulation, classrooms)
                else:
                    newp = self.crossover(newPopulation)
                newPopulation.append(newp)
            self.population = newPopulation
            result = {
                course.course_id: {
                    'teacher': str(course.course_teacher),
                    'time': str(course.course_time),
                    'classroom': str(course.course_classroom.classroom_id),
                } for course in bestcourses
            }
            with open(save_path, 'w', encoding='utf8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        return bestcourses
