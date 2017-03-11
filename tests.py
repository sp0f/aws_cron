from scheduler import *
from time import strptime

def test_schedule(schedule, start_time):
    answer=should_i_run_complex(schedule,start_time)
    print "start: {} {} {} {} {} vs. schedule: {} = {}".format(start_time.tm_min, start_time.tm_hour, start_time.tm_mday,
                                                               start_time.tm_mon, start_time.tm_wday, schedule, answer)

# scheduler tests - BASIC
start_time=strptime("28 12 2016 18:56:00", "%d %m %Y %H:%M:%S")

print "BASIC"
schedule="56 * * * *"
test_schedule(schedule, start_time)
schedule="1 * * * *"
test_schedule(schedule, start_time)


schedule="56 18 * * *"
test_schedule(schedule, start_time)
schedule="56 19 * * *"
test_schedule(schedule, start_time)
schedule="1 19 * * *"
test_schedule(schedule, start_time)

schedule="56 18 28 * *"
test_schedule(schedule, start_time)
schedule="56 18 29 * *"
test_schedule(schedule, start_time)
schedule="1 19 31 * *"
test_schedule(schedule, start_time)

schedule="56 18 28 12 *"
test_schedule(schedule, start_time)
schedule="56 18 28 3 *"
test_schedule(schedule, start_time)
schedule="1 19 31 4 *"
test_schedule(schedule, start_time)

schedule="56 18 28 12 2"
test_schedule(schedule, start_time)
schedule="56 18 28 12 3"
test_schedule(schedule, start_time)
schedule="1 19 31 4 6"
test_schedule(schedule, start_time)

print "RANGES"
schedule="56-58 * * * *"
test_schedule(schedule, start_time)
schedule="45-58 * * * *"
test_schedule(schedule, start_time)
schedule="45-56 * * * *"
test_schedule(schedule, start_time)
schedule="56-56 * * * *"
test_schedule(schedule, start_time)
schedule="45-55 * * * *"
test_schedule(schedule, start_time)

schedule="56-58 17-18 12-28 1-12 0-3"
test_schedule(schedule, start_time)
schedule="56-58 17-18 12-28 1-12 0-1"
test_schedule(schedule, start_time)

print "LISTS"
schedule="3,4,56 * * * *"
test_schedule(schedule, start_time)
schedule="56,2,1 * * * *"
test_schedule(schedule, start_time)
schedule="2,56,1 * * * *"
test_schedule(schedule, start_time)
schedule="1,2,3,4,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39" \
         ",40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59 * * * *"
test_schedule(schedule, start_time)
schedule="1,2,3,4,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39" \
         ",40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,57,58,59 * * * *"
test_schedule(schedule, start_time)

print "STEPS"
schedule="*/2 * * * *"
test_schedule(schedule, start_time)
schedule="*/3 * * * *"
test_schedule(schedule, start_time)
schedule="*/28 * * * *"
test_schedule(schedule, start_time)
schedule="*/56 * * * *"
test_schedule(schedule, start_time)
# TODO catch that
#schedule="*/0 * * * *"
#test_schedule(schedule, start_time)
schedule="*/56 */2 */1 */6 */2"
test_schedule(schedule, start_time)

print "STEPS+RANGES"
schedule="48-58/2 * * * *"
test_schedule(schedule, start_time)
schedule="24-56/2 * * * *"
test_schedule(schedule, start_time)
schedule="56-58/2 * * * *"
test_schedule(schedule, start_time)
schedule="56-58/28 * * * *"
test_schedule(schedule, start_time)

schedule="24-55/2 * * * *"
test_schedule(schedule, start_time)
schedule="17-59/27 * * * *"
test_schedule(schedule, start_time)
schedule="56-11/2 * * * *"
test_schedule(schedule, start_time)
