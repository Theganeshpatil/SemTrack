# Create events of all courses

courses = ["CBS 311 Database Security" "IEC 312 Distributed System Security" "CBS 312 Network Security, IoT, and Wireless Security" "CBE 311 Fundamentals of Data Science" "IMA 313 Number Theory and Mathematical Theory of Coding" "IHS 314 Financial Crime, Motivations, and Typologies" "CBE 312 Introduction to Artificial Intelligence"]

semster_class_start_date = "2023-08-02"
semester_class_end_date = "2023-11-13"

To create all classes events in whole semester:

## Classes

    1. Mon, Tue | 9.00-9.55 AM | 'CBS 311 LS'
    2. Wed | 9.00-9.55 AM | 'CBS 312 GBC'
    3. Thr | 9.00-9.55 AM | 'IMA 313 BA'
    4. Fri | 9.00-9.55 AM | 'IEC 312 ES'
    5. Wed | 10.00-10.55 AM | 'IMA 313 BA'
    6. Thr | 10.00-10.55 AM | 'CBS 312 GBC'
    7. Fri | 10.00-10.55 AM | 'IHS 314 SKJ'
    8. Mon | 10.00-10.55 AM | 'CBE 311 VP'
    9. Thr | 11.05-12.00 PM | 'IHS 314 SKJ'
    10. Fri | 11.05-12.00 PM | 'CBS 312 GBC'
    11. Mon | 12.05-1.00 PM | 'CBS 311 LS'
    12. Tue | 12.05-1.00 PM | 'IEC 312 ES'
    13. Wed | 12.05-1.00 PM | 'CBE 311 VP'
    14. Thu | 12.05-1.00 PM | 'CBE 312 ER'
    15. Fri | 12.05-1.00 PM | 'IMA 313 BA'
    16. Mon | 2.00-2.55 PM | 'IEC 312 ES'
    17. Tue | 2.00-2.55 PM | 'CBE 311 VP'
    18. Wed | 2.00-2.55 PM | 'IHS 314 SKJ'

## Labs

    19. Mon | 3.00-5.00 PM | 'CBE 311 LAB VP'
    20. Tue | 3.00-5.00 PM | 'IEC 312 LAB ES'
    21. Wed | 3.00-5.00 PM | 'CBS 312 LAB GBC'

# Remove classes on Holidays

holidays = ["2023-08-15", "2023-08-29", "2023-09-27", "2023-10-02", "2023-10-23", "2023-10-24", "2023-11-12"]

- Now calculate no of sessions held in a semester
  no_of_sessions_of_each_course = (int)
  add desc of "Attended" in each event.
  If you are not attending a class on perticular day you will change a desc of that perticular event

Functions:

1. Create Course Events

- Delete All holidays
- Update their description to attended

2. Delete All Events
3. Get Events (Upcoming )
4. Get Attendance
5. Get Maximum Possible Attendance
6. Delete Events on Date (Used in deleting holidays)
7. Mark Absent for Events on Date
