import numpy as np

#星期优先级
weight_day = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
#时间段的优先级
weight_section = [1.0]*14
#课程类型优先级
priority_course = [1]*6

def schedule_score(population, constraints, elite_num):
    '''
    population :第一维是种群，第二维课程
    contraints : 约束列表
    elite：精英数量
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
                #同一教室同一时间冲突
                if p[i].course_classroom==p[j].course_classroom:
                    for timeA in p[i].course_time:
                        for timeB in p[j].course_time:
                            if timeA.week==timeB.week and timeA.day==timeB.day and \
                                timeA.class_num==timeB.class_num:
                                confict += 1
                #同一老师同一时间冲突
                if p[i].course_teacher == p[j].course_teacher:
                    for timeA in p[i].course_time:
                        for timeB in p[j].course_time:
                            if timeA.week == timeB.week and timeA.day == timeB.day and \
                                    timeA.class_num == timeB.class_num:
                                confict += 1
        conficts.append(confict)

    for courses in population:
        scores.append(timetable_score(courses, constraints))

    for hard, soft in zip(conficts,scores):
        final_scores.append(hard_weight*hard+soft_weight*soft)
    index = np.array(final_scores).argsort()

    return index[:elite_num], final_scores[index[0]]








def timetable_score(courses, constraints):
    '''
    计算整个课表的得分
    '''
    scores = []
    for course, constraint in zip(courses, constraints):
        unweighted_score = course_score(course, constraint)
        weighted_score = unweighted_score * priority_course(course)
        scores.append(weighted_score)
    return sum(scores)




def priority_course(course):
    t1 = 1.0
    t2 = 1.0
    t3 = 1.0
    # TODO 课程类型要再对一下
    priority = t1 * course.course_hour + t2 * priority_course[course.course_type] \
               + t3*course.course_max_capacity
    return priority



def course_score(course,constraint, alpha=1.0,beta=1.0, gamma=1.0):
    """
    计算单个课程的得分
    """
    #计算时间得分
    times = course.course_time
    score_day = 0.0
    score_section = 0.0
    for time in times:
        score_day += weight_day[time.day-1]
        score_section += weight_section[time.class_num-1]

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
    # if constraint.course_continue:
        #太难了先没写

        # sections = times.class_num
        # sections = np.array(sections)
    #是否单双周
    if constraint.course_is_odd_week:
        weeks_set = list(set(weeks))
        weeks_list = np.sort(np.array(weeks_set))
        odd_flag = False
        for i,num in enumerate(weeks_list):
            if i==len(weeks_list)-1:
                odd_flag = True
                break
            if weeks_list[i+1]-weeks_list[i]!=2:
                break
        if odd_flag:
            score_constraint += 12
    #每周最大/最小排课天数
    if constraint.course_biggest_day_number!=-1 or constraint.course_smallest_day_number!=-1:
        max_day = -1
        min_day = 1e9
        cur_day = set()
        pre_week = weeks[0]
        for i in range(len(weeks)):
            if weeks[i]==pre_week:
                cur_day.add(days[i])
                pre_week = weeks[i]
            else:
                max_day = max(max_day, len(cur_day))
                min_day = min(min_day, len(cur_day))
                cur_day = set()
                cur_day.add(days[i])
                pre_week = weeks[i]
        if constraint.course_biggest_day_number!=-1:
            if max_day <= constraint.course_biggest_day_number:
                score_constraint += 8
        if constraint.course_smallest_day_number!=-1:
            if min_day >= constraint.course_smallest_day_number:
                score_constraint += 9
    # TODO 完善别的约束


    #计算教室容量得分
    score_room = 0.0
    classroom = course.course_classroom
    score_room += classroom.classroom_capacity - course.course_max_capacity

    score = alpha * score_time + beta * score_constraint - gamma * score_room
    return score










