import numpy as np
import collections

# 星期优先级
weight_day = collections.defaultdict(lambda: 1.0)
weight_day[6] = 2
weight_day[7] = 2

# 时间段的优先级
weight_section = collections.defaultdict(lambda: 1.0)

# 课程类型优先级
priority_course_type = collections.defaultdict(lambda: 1.0)

#约束优先级定义
odd_week_priority = 12
course_biggest_day_number_priority = 8
course_smallest_day_number_priority  = 9

def schedule_score(population, elite_num):
    '''
    population: 第一维是种群，第二维课程
    contraints: 约束列表
    elite: 精英数量
    '''
    conficts = []
    scores  = []
    final_scores = []
    hard_weight = 10000
    soft_weight = 1
    n = len(population[0])
    for p in population:
        confict = 0
        #自身排课就冲突
        for i in range(0, n-1):
            times = p[i].course_time
            hours = len(times)
            for index1 in range(0,hours-1):
                for index2 in range(index1+1, hours):
                    if times[index1].week==times[index2].week \
                        and times[index1].day==times[index2].day \
                        and times[index1].class_num==times[index2].class_num:
                        confict+=1
            #不同课程冲突
            for j in range(i+1, n):
                for timeA in p[i].course_time:
                    for timeB in p[j].course_time:
                        if timeA.week==timeB.week and timeA.day==timeB.day \
                            and timeA.class_num==timeB.class_num:
                            #同一教室同一时间冲突
                            if p[i].course_classroom.classroom_id==p[j].course_classroom.classroom_id:
                                confict += 1
                            #同一老师同一时间冲突
                            for pi_teacher in p[i].course_teacher:
                                for pj_teacher in p[j].course_teacher:
                                    if pi_teacher == pj_teacher:
                                        confict += 1
        conficts.append(confict)

    for courses in population:
        scores.append(timetable_score(courses))

    for hard, soft in zip(conficts,scores):
        final_scores.append(hard_weight*hard+soft_weight*soft)
    index = np.array(final_scores).argsort()

    return index[:elite_num], final_scores[index[0]]


def timetable_score(courses):
    '''
    计算整个课表的得分
    '''
    scores = []
    for course in courses:
        unweighted_score = course_score(course)
        weighted_score = unweighted_score * priority_course(course)
        scores.append(weighted_score)
    return sum(scores)


def priority_course(course):
    t1 = 1.0
    t2 = 1.0
    t3 = 1.0
    # TODO 课程类型要再对一下
    priority = t1 * course.course_hour + t2 * priority_course_type[course.course_type] \
               + t3*course.course_max_capacity
    return priority


def course_score(course, alpha=1.0,beta=1.0, gamma=1.0):
    """
    计算单个课程的得分
    """
    #计算时间得分
    times = course.course_time
    score_day = 0.0
    score_section = 0.0
    for time in times:
        score_day += weight_day[time.day]
        score_section += weight_section[time.class_num]

    score_time = score_day + score_section #暂时没考虑星期和节的权重差别

    #计算约束得分
    weeks = []
    days = []
    sections = []
    for time in times:
        weeks.append(time.week)
        days.append(time.day)
        days.append(sections)
    score_constraint = 0.0
    #是否连堂
    # if course_constraint.course_continue:
        #太难了先没写

        # sections = times.class_num
        # sections = np.array(sections)
    #是否单双周
    if course.course_constraint.course_is_odd_week:
        if is_odd_week(weeks):
            score_constraint += odd_week_priority
    #每周最大/最小排课天数
    if course.course_constraint.course_biggest_day_number!=-1 or course.course_constraint.course_smallest_day_number!=-1:
        max_day, min_day = get_max_min_day(weeks, days)
        if course.course_constraint.course_biggest_day_number!=-1:
            if max_day <= course.course_constraint.course_biggest_day_number:
                score_constraint += course_biggest_day_number_priority
        if course.course_constraint.course_smallest_day_number!=-1:
            if min_day >= course.course_constraint.course_smallest_day_number:
                score_constraint += course_smallest_day_number_priority
    # TODO 完善别的约束


    #计算教室容量得分
    score_room = 0.0
    classroom = course.course_classroom
    score_room += classroom.classroom_capacity - course.course_max_capacity

    score = alpha * score_time + beta * score_constraint - gamma * score_room
    return score

def is_odd_week(weeks):
    weeks_set = list(set(weeks))
    weeks_list = np.sort(np.array(weeks_set))
    odd_flag = False
    for i, num in enumerate(weeks_list):
        if i == len(weeks_list) - 1:
            odd_flag = True
            break
        if weeks_list[i + 1] - weeks_list[i] != 2:
            break
    return odd_flag

def get_max_min_day(weeks, days):
    max_day = -1
    min_day = 1e9
    cur_day = set()
    pre_week = weeks[0]
    for i in range(len(weeks)):
        if weeks[i] == pre_week:
            cur_day.add(days[i])
            pre_week = weeks[i]
        else:
            max_day = max(max_day, len(cur_day))
            min_day = min(min_day, len(cur_day))
            cur_day = set()
            cur_day.add(days[i])
            pre_week = weeks[i]
    return max_day, min_day