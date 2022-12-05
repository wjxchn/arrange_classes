import copy
import numpy as np

from db.models import User, Student, Teacher, Admin, Course, Course_constraint, Classroom, Course_table

class MyTime:
    def __init__(self, semester=None, week=None, day=None, class_num=None) -> None:
        self.semester = semester
        self.week = week
        self.day = day
        self.class_num = class_num
    def __repr__(self) -> str:        
        return '-'.join([self.semester, str(self.week), str(self.day), str(self.class_num)])

def rand_classroom(course, roomRange=50):
    res = Classroom()
    res.classroom_id = np.random.randint(1, roomRange+1)
    return res

def rand_time(course, semester_range='2021-1', week_range=(1, 16), day_range=(1, 7), class_num_range=(1, 14), num=1):
    if num == 1:
        res = MyTime()
        res.semester = semester_range
        res.week = np.random.randint(week_range[0], week_range[1] + 1)
        res.day = np.random.randint(day_range[0], day_range[1] + 1)
        res.class_num = np.random.randint(class_num_range[0], class_num_range[1] + 1)
    else:
        res = []
        for week in week_range:
            for day in day_range:
                for class_num in class_num_range:
                    res.append((week, day, class_num))
        np.random.shuffle(res)
        res = [MyTime(semester=semester_range, week=week, day=day, class_num=class_num) for week, day, class_num in res]
    
    return res

def random_schedule(course: Course, ):
    course._time = sorted(rand_time(course, num=course.course_hour))
    course._classroom = rand_classroom(course)
    return course

def judge_teacher_conflict(a, b, self=False):
    a = Course.course_teacher.through.objects.filter(course_id=a)
    b = Course.course_teacher.through.objects.filter(course_id=b)
    for i, s in enumerate(a):
        for j, t in enumerate(b):
            if self and i == j:
                continue
            if (s.teacher_id) == (t.teacher_id):
                return True
    return False

def judge_time_conflict(a, b, self=False):
    for i, s in enumerate(a):
        for j, t in enumerate(b):
            if self and i == j:
                continue
            if (s.semester, s.week, s.day, s.class_num) == (t.semester, t.week, t.day, t.class_num):
                return True
    return False

def static_schedule_cost(population, elite):
    conflicts = []
    n = len(population[0])
    for p in population:
        hard_conflict, soft_conflict = 0, 0
        for i in range(0, n):
            if judge_time_conflict(p[i]._time, p[i]._time, self=True):
                hard_conflict += 100
            for j in range(0, i):
                if judge_time_conflict(p[i]._time, p[j]._time):
                    if p[i]._classroom.classroom_id == p[j]._classroom.classroom_id:
                        hard_conflict += 1
                    
                    if judge_teacher_conflict(p[i].course_id, p[j].course_id):
                        hard_conflict += 1


        conflicts.append(hard_conflict * 10000 + soft_conflict)
    index = np.array(conflicts).argsort()
    return index[: elite], conflicts[index[0]]

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
    def init_population(self, courses, roomRange):
        self.population = []
        for _ in range(self.popsize):
            entity = []
            for course in courses:
                course = random_schedule(course)
                entity.append(copy.deepcopy(course))
            self.population.append(entity)
            
    #变异
    def mutate(self, eiltePopulation, roomRange):
        #选择变异的个数
        e = np.random.randint(0, self.elite, 1)[0]
        ep = copy.deepcopy(eiltePopulation[e])
        for p in ep:
            pos = np.random.randint(0, len(p._time) + 1, 1)[0]
            if pos == 0:
                p._classroom = rand_classroom(p)
            else:
                p._time[pos - 1] = rand_time(p)
                p._time = sorted(p._time)
        return ep

    def change(self, value, valueRange):
        value = np.random.randint(1, valueRange+1, 1)[0]
        return value

    def crossover(self, eiltePopulation):
        e1 = np.random.randint(0, self.elite, 1)[0]
        e2 = np.random.randint(0, self.elite, 1)[0]
        pos = np.random.randint(0, 2, 1)[0]
        ep1 = copy.deepcopy(eiltePopulation[e1])
        ep2 = eiltePopulation[e2]
        for p1, p2 in zip(ep1, ep2):
            if pos == 0:
                p1._time = p2._time
            if pos == 1:
                p1._classroom = p2._classroom
        return ep1

    def evolution(self, courses, roomRange=100):
        bestScore = 0
        bestcourses = None
        self.init_population(courses, roomRange)
        for i in range(self.maxiter):
            eliteIndex, bestScore = static_schedule_cost(self.population, self.elite)
            print('Iter: {} | conflict: {}'.format(i + 1, bestScore))
            if bestScore == 0:
                bestcourses = self.population[eliteIndex[0]]
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
