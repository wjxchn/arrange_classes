

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

# 约束优先级定义
odd_week_priority = 12  #单双周
course_continuous_priority = 10 #连堂
course_biggest_day_number_priority = 8 #每周最大排课天数
course_smallest_day_number_priority = 9 #每周最少排课天数
weekend_priority = 5  #是否可在周末上课
course_smallest_sections_priority = 6 #每天最小上课节数
course_biggest_sections_priority = 7 #每天最大上课节数
no_course_sections_priority = 4 #不可排课的节数
capacity_ratio_priority = 11 #课程容量和教室容量的比例



def schedule_score(population, elite_num):
    '''
    population: 第一维是种群，第二维课程
    contraints: 约束列表
    elite: 精英数量
    '''
    conficts = []
    scores = []
    final_scores = []
    hard_weight = 1e9
    soft_weight = 1
    n = len(population[0])
    for pid, p in enumerate(population):
        confict = 0
        # 不同课程冲突
        mp = collections.defaultdict(
            lambda: {
                'classroom': collections.defaultdict(lambda: 0),
                'teacher': collections.defaultdict(lambda: 0),
            }
        )
        for i in range(0, n):
            # 自身排课就冲突
            mp2 = collections.defaultdict(lambda: 0)
            for time in p[i].course_time:
                confict += mp2[time]
                mp2[time] += 1

            
            for time in p[i].course_time:
                # 教室冲突
                confict += mp[time.class_num_for_semester()]['classroom'][p[i].course_classroom.classroom_id]
                mp[time.class_num_for_semester()]['classroom'][p[i].course_classroom.classroom_id] += 1

                # 教师冲突
                for teacher_id in p[i].course_teacher:
                    confict += mp[time.class_num_for_semester()]['teacher'][teacher_id]
                    mp[time.class_num_for_semester()]['teacher'][teacher_id] += 1

        conficts.append(confict)

    for courses in population:
        scores.append(timetable_score(courses))

    for hard, soft in zip(conficts, scores):
        final_scores.append(hard_weight * hard + soft_weight * soft)
    index = np.array(final_scores).argsort()

    return index[:elite_num], final_scores[index[0]]


def timetable_score(courses):
    '''
    计算整个课表的得分
    '''
    scores = []
    for course in courses:
        unweighted_score = course_score(course)
        weighted_score = -1 * unweighted_score * priority_course(course)
        scores.append(weighted_score)
    return sum(scores)


def priority_course(course):
    t1 = 1.0
    t2 = 1.0
    t3 = 1.0
    # TODO 课程类型要再对一下
    priority = t1 * course.course_hour + t2 * priority_course_type[course.course_type] \
               + t3 * course.course_max_capacity
    return priority


# TODO 这里参数要调
def course_score(course, alpha=1.0, beta=1.0, gamma=1.0):
    """
    计算单个课程的得分
    """
    # 计算时间得分
    times = course.course_time
    times = sorted(times)

    score_day = 0.0
    score_section = 0.0
    for time in times:
        score_day += weight_day[time.day]
        score_section += weight_section[time.class_num]

    score_time = score_day + score_section  # 暂时没考虑星期和节的权重差别

    # 计算约束得分
    weeks = []
    days = []
    sections = []
    for time in times:
        weeks.append(time.week)
        days.append(time.day)
        sections.append(time.class_num)
    score_constraint = 0.0

    # 是否连堂
    if course.course_constraint.course_continue:
        if is_course_continuous(weeks,days,sections):
            score_constraint += course_continuous_priority

    # 是否单双周
    if course.course_constraint.course_is_odd_week:
        if is_odd_week(weeks):
            score_constraint += odd_week_priority
    # 每周最大/最小排课天数
    if course.course_constraint.course_biggest_day_number != -1 or course.course_constraint.course_smallest_day_number != -1:
        max_day, min_day = get_max_min_day(weeks, days)
        if course.course_constraint.course_biggest_day_number != -1:
            if max_day <= course.course_constraint.course_biggest_day_number:
                score_constraint += course_biggest_day_number_priority
        if course.course_constraint.course_smallest_day_number != -1:
            if min_day >= course.course_constraint.course_smallest_day_number:
                score_constraint += course_smallest_day_number_priority
    #是否可在周末排课
    if course.course_constraint.course_can_weekends and is_course_weekend(days):
        score_constraint += weekend_priority
    elif not course.course_constraint.course_can_weekends and not is_course_weekend(days):
        score_constraint += weekend_priority

    # 每天最小/最大排课节数
    if course.course_constraint.course_smallest_sections!=-1 or course.course_constraint.course_biggest_sections!=-1:
        max_sections, min_sections = get_max_min_course(weeks,days)
        if course.course_constraint.course_biggest_sections!=-1:
            if max_sections<=course.course_constraint.course_biggest_sections:
                score_constraint += course_biggest_sections_priority
        if course.course_constraint.course_smallest_sections!=-1:
            if min_sections >= course.course_constraint.course_smallest_sections:
                score_constraint += course_smallest_sections_priority

    # 每天不上课的节数
    if len(course.course_constraint.course_no_sections)>0:
        no_list = course.course_constraint.course_no_sections
        if no_course_section(sections,no_list):
            score_constraint += no_course_sections_priority

    # 课程容量和教室容量的比例
    #情景分析 教师容量一定是大于课程容量的，适用场景是 老师不希望教室太空，也就是不希望此比例太小
    #感觉命名上来说应该改为min, 先当成min用了
    if course.course_constraint.max_course_room_ratio!=-1:
        ratio = capacity_ratio(course,course.course_classroom)
        if ratio>=course.course_constraint.max_course_room_ratio:
            score_constraint += capacity_ratio_priority


    # 计算教室容量得分
    score_room = 0.0
    classroom = course.course_classroom
    score_room += classroom.classroom_capacity - course.course_max_capacity

    score = alpha * score_time + beta * score_constraint - gamma / 100.0 * score_room
    return score


def is_odd_week(weeks):
    '''
    是否单双周
    '''
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


def is_course_continuous(weeks, days, sections):
    #是否连堂
    res = True
    length = 2
    pre_week = -1
    pre_day = -1
    pre_section = -1
    for i in range(len(weeks)):
        if pre_week == weeks[i] and pre_day == days[i] and pre_section + 1 == sections[i]:
            length += 1
        else:
            if length < 2:
                res = False
                break
            else:
                length = 1
        pre_week = weeks[i]
        pre_day = days[i]
        pre_section = sections[i]
    return res



def is_course_weekend(days):
    # 周末是否有课
    for day in days:
        if day == 6 or day == 7:
            return True
    return False


def get_max_min_course(weeks, days):
    '''
    每天最小/最大上课节数
    '''
    max_course = -1
    min_course = 1e9
    pre_week = weeks[0]
    pre_day = days[0]
    num = 0
    for i in range(len(weeks)):
        if weeks[i] == pre_week and days[i] == pre_day:
            # print(1)
            num += 1
            max_course = max(max_course, num)
        else:
            # print(2)
            min_course = min(min_course, num)
            pre_week = weeks[i]
            pre_day = days[i]
            num = 1
    min_course = min(min_course, num)
    return max_course, min_course



def no_course_section(sections, no_sections):
    # 每天不上课的节数
    for sec in no_sections:
        if sec in sections:
            return False
    return True


def capacity_ratio(course, classroom):
    # 课程容量和教室容量比值
    ratio = course.course_max_capacity / classroom.classroom_capacity
    return ratio


def get_max_min_day(weeks, days):
    '''
    返回每周最大上课天数 和 每周最小上课天数
    '''
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

