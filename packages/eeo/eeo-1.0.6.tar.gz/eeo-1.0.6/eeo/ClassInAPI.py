# -*- coding: utf-8 -*-
"""
@Author   : QH
@Time     :2024/7/2
@File     :ClassInAPI.py
@IDE      :PyCharm
"""

import time
import hashlib
import requests
import json

"""
如果你有任何疑问，可以通过eeoapisupport@eeoa.com联系我们

If you have any questions you can contact us at eeoapisupport@eeoa.com

ClassIn APIDoc：https://docs.eeo.cn/api/  
"""


# 请求域名
domain = 'https://api.eeo.cn'


class Path:
    def __init__(self):
        # 用户相关接口
        self.register = domain + '/partner/api/course.api.php?action=register'
        self.registerMultiple = domain + '/partner/api/course.api.php?action=registerMultiple'
        self.modifyPassword = domain + '/partner/api/course.api.php?action=modifyPassword'
        self.addSchoolStudent = domain + '/partner/api/course.api.php?action=addSchoolStudent'
        self.editSchoolStudent = domain + '/partner/api/course.api.php?action=editSchoolStudent'
        self.addTeacher = domain + '/partner/api/course.api.php?action=addTeacher'
        self.editTeacher = domain + '/partner/api/course.api.php?action=editTeacher'
        self.stopUsingTeacher = domain + '/partner/api/course.api.php?action=stopUsingTeacher'
        self.restartUsingTeacher = domain + '/partner/api/course.api.php?action=restartUsingTeacher'

        # 课程相关接口
        self.addCourse = domain + '/partner/api/course.api.php?action=addCourse'
        self.editCourse = domain + '/partner/api/course.api.php?action=editCourse'
        self.endCourse = domain + '/partner/api/course.api.php?action=endCourse'
        self.modifyCourseTeacher = domain + '/partner/api/course.api.php?action=modifyCourseTeacher'
        self.removeCourseTeacher = domain + '/partner/api/course.api.php?action=removeCourseTeacher'

        # 课节相关接口
        self.addCourseClass = domain + '/partner/api/course.api.php?action=addCourseClass'
        self.addCourseClassMultiple = domain + '/partner/api/course.api.php?action=addCourseClassMultiple'
        self.editCourseClass = domain + '/partner/api/course.api.php?action=editCourseClass'
        self.delCourseClass = domain + '/partner/api/course.api.php?action=delCourseClass'
        self.modifyClassSeatNum = domain + '/partner/api/course.api.php?action=modifyClassSeatNum'

        # 操作课程或课节学生
        self.addCourseStudent = domain + '/partner/api/course.api.php?action=addCourseStudent'
        self.delCourseStudent = domain + '/partner/api/course.api.php?action=delCourseStudent'
        self.addCourseStudentMultiple = domain + '/partner/api/course.api.php?action=addCourseStudentMultiple'
        self.delCourseStudentMultiple = domain + '/partner/api/course.api.php?action=delCourseStudentMultiple'
        self.addClassStudentMultiple = domain + '/partner/api/course.api.php?action=addClassStudentMultiple'
        self.delClassStudentMultiple = domain + '/partner/api/course.api.php?action=delClassStudentMultiple'
        self.addCourseClassStudent = domain + '/partner/api/course.api.php?action=addCourseClassStudent'

        # 机构标签
        self.addSchoolLabel = domain + '/partner/api/course.api.php?action=addSchoolLabel'
        self.updateSchoolLabel = domain + '/partner/api/course.api.php?action=updateSchoolLabel'
        self.deleteSchoolLabel = domain + '/partner/api/course.api.php?action=deleteSchoolLabel'

        # 课程课节标签相关
        self.addCourseLabels = domain + '/partner/api/course.api.php?action=addCourseLabels'
        self.addClassLabels = domain + '/partner/api/course.api.php?action=addClassLabels'

        # 同步班级昵称
        self.modifyGroupMemberNickname = domain + '/partner/api/course.api.php?action=modifyGroupMemberNickname'

        # 云盘相关
        self.getFolderList = domain + '/partner/api/cloud.api.php?action=getFolderList'
        self.getCloudList = domain + '/partner/api/cloud.api.php?action=getCloudList'
        self.getTopFolderId = domain + '/partner/api/cloud.api.php?action=getTopFolderId'
        self.uploadFile = domain + '/partner/api/cloud.api.php?action=uploadFile'
        self.renameFile = domain + '/partner/api/cloud.api.php?action=renameFile'
        self.delFile = domain + '/partner/api/cloud.api.php?action=delFile'
        self.createFolder = domain + '/partner/api/cloud.api.php?action=createFolder'
        self.renameFolder = domain + '/partner/api/cloud.api.php?action=renameFolder'
        self.delFolder = domain + '/partner/api/cloud.api.php?action=delFolder'

        # 直播相关接口
        self.setClassVideoMultiple = domain + '/partner/api/course.api.php?action=setClassVideoMultiple'
        self.deleteClassVideo = domain + '/partner/api/course.api.php?action=deleteClassVideo'
        self.updateClassLockStatus = domain + '/partner/api/course.api.php?action=updateClassLockStatus'
        self.getWebcastUrl = domain + '/partner/api/course.api.php?action=getWebcastUrl'

        # 唤醒客户端进入教室
        self.getLoginLinked = domain + '/partner/api/course.api.php?action=getLoginLinked'


class API:
    def __init__(self, school_uid, school_secret):
        """
        初始化eeo api对象，需传输eeo的SID和SECRET
        :param school_uid: eeo 学校账号UID
        :param school_secret: 密钥
        """

        self.SID = school_uid
        self.secret = school_secret
        # 创建请求url的对象
        self.action = Path()

    def get_safe_key(self):
        timeStamp = int(time.time())
        safeKey = hashlib.md5(f'{self.secret}{timeStamp}'.encode()).hexdigest()
        return timeStamp, safeKey

    def register(self, account, nickname, password, addToSchoolMember):
        """
        注册用户  https://docs.eeo.cn/api/zh-hans/user/register.html
        @param account: string 必填-用户手机号或邮箱
        @param nickname: string 非必填-eeo.cn姓名，如用户是首次注册，将同步姓名信息至客户端昵称，非首次注册则不修改用户当前昵称
        @param password:string 必填-密码
        @param addToSchoolMember:int 非必填-1学生 2老师
        @return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'email': account,
            'telephone': account,
            'password': password,
            'nickname': nickname,
            'addToSchoolMember': addToSchoolMember
        }
        if '@' in account:
            del payload['telephone']
        else:
            del payload['email']

        response = requests.post(url=self.action.register, data=payload).json()

        return response

    def register_multiple(self, userJson):
        """
        批量注册用户  https://docs.eeo.cn/api/zh-hans/user/registerMultiple.html
        @param userJson:
        telephone和email 2选1
        [
        {"telephone":"xxxx","nickname":"xxxx","password":"xxxx"},
        {"email":"xxxx","nickname":"xxxx","password":"xxxx"}
        ]
        @return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'userJson': json.dumps(userJson)
        }

        response = requests.post(url=self.action.registerMultiple, data=payload).json()

        return response

    def modify_password(self, uid, oldMd5pass, password=None, md5pass=None):
        """
        修改用户密码  https://docs.eeo.cn/api/zh-hans/user/modifyPassword.html
        password 与md5pass 2选1   如果都传以md5pass为准
        :param uid: UID
        :param oldMd5pass: 32位小写	原MD5密码
        :param password:是 6-20位，不符合会报错
        :param md5pass:32位MD5 小写
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'uid': uid,
            'oldMd5pass': oldMd5pass,
            'password': password,
            'md5pass': md5pass,
        }
        if md5pass is None:
            del payload['md5pass']
        if password is None:
            del payload['password']
        if md5pass is not None and password is not None:
            del payload['password']

        response = requests.post(url=self.action.modifyPassword, data=payload).json()

        return response

    def add_teacher(self, teacherAccount, teacherName):
        """
        添加学校老师  https://docs.eeo.cn/api/zh-hans/user/addTeacher.html
        :param teacherAccount:string 老师账号
        :param teacherName:string 老师姓名
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'teacherAccount': teacherAccount,
            'teacherName': teacherName
        }

        response = requests.post(url=self.action.addTeacher, data=payload).json()
        return response

    def edit_teacher(self, teacherUid, teacherName):
        """
        编辑老师信息  https://docs.eeo.cn/api/zh-hans/user/editTeacher.html
        :param teacherUid:用户UID
        :param teacherName:string 老师姓名
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'teacherUid': teacherUid,
            'teacherName': teacherName
        }

        response = requests.post(url=self.action.editTeacher, data=payload).json()
        return response

    def stop_using_teacher(self, teacherUid):
        """
        停用老师  https://docs.eeo.cn/api/zh-hans/user/stopUsingTeacher.html
        :param teacherUid: 用户UID
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'teacherUid': teacherUid,
        }

        response = requests.post(url=self.action.stopUsingTeacher, data=payload).json()
        return response

    def restart_using_teacher(self, teacherUid):
        """
        启用老师  https://docs.eeo.cn/api/zh-hans/user/restartUsingTeacher.html
        :param teacherUid: 用户UID
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'teacherUid': teacherUid,
        }

        response = requests.post(url=self.action.restartUsingTeacher, data=payload).json()
        return response

    def add_school_student(self, studentAccount, studentName):
        """
        添加学校学生  https://docs.eeo.cn/api/zh-hans/user/addSchoolStudent.html
        :param studentAccount:string 学生账号
        :param studentName:string 学生姓名
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'studentAccount': studentAccount,
            'studentName': studentName
        }

        response = requests.post(url=self.action.addSchoolStudent, data=payload).json()

        return response

    def edit_school_student(self, studentUid, studentName):
        """
        添加学校学生  https://docs.eeo.cn/api/zh-hans/user/editSchoolStudent.html
        :param studentUid: 用户UID
        :param studentName:string 学生姓名
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'studentUid': studentUid,
            'studentName': studentName
        }

        response = requests.post(url=self.action.editSchoolStudent, data=payload).json()

        return response

    def add_course(self, courseName, folderId=None, expiryTime=None, mainTeacherUid=None, allowAddFriend=None,
                   subjectId=None, allowStudentModifyNickname=None, notAllowDeleteCourseStudentReplay=None,
                   courseUniqueIdentity=None):
        """
        创建课程  https://docs.eeo.cn/api/zh-hans/classroom/addCourse.html
        :param courseName: string 必填，课程名
        :param folderId: int 非必填，授权云盘文件夹ID
        :param expiryTime: int时间戳, 非必填，课程有效期，默认空永久有效，
        :param mainTeacherUid: int非必填，班主任uid，默认空
        :param subjectId: int 课程学科分类	0:空; 1:语文; 2:数学; 3:英语; 4:物理; 5:化学; 6:生物; 7:政治; 8:历史; 9:地理; 10:思想品德; 11:音乐; 12:体育; 13:美术; 14:通用技术; 15:信息技术; 16:科学; 99:其他学科
        :param allowAddFriend: int非必填，是否允许班级成员在群里互相添加好友，0=不允许，1=允许，传非0或非1报参数错误
        :param allowStudentModifyNickname:int非必填，是否允许学生在群里修改其班级昵称，0=不允许，1=允许，传非0或非1报参数错误，不传默认0
        :param notAllowDeleteCourseStudentReplay: string  是否不允许离开班级的学生或班级解散后，可查看课程内容 0=否（允许），1=是（不允许）
        :param courseUniqueIdentity: string非必填，机构可传唯一标识，传入此值后，我们会检验已创建课程中是否有该唯一标识
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseName': courseName,
            'folderId': folderId,
            'expiryTime': expiryTime,
            'mainTeacherUid': mainTeacherUid,
            'subjectId': subjectId,
            'allowAddFriend': allowAddFriend,
            'allowStudentModifyNickname': allowStudentModifyNickname,
            'notAllowDeleteCourseStudentReplay': notAllowDeleteCourseStudentReplay,
            'courseUniqueIdentity': courseUniqueIdentity,
        }

        response = requests.post(url=self.action.addCourse, data=payload).json()
        return response

    def edit_course(self, courseId, courseName, folderId=None, expiryTime=None, mainTeacherUid=None, subjectId=None,
                    allowAddFriend=None, allowStudentModifyNickname=None, notAllowDeleteCourseStudentReplay=None,
                    courseUniqueIdentity=None):
        """
        编辑课程  https://docs.eeo.cn/api/zh-hans/classroom/editCourse.html
        :param courseId: string 必填，课程ID
        :param courseName: string 非必填，课程名
        :param folderId: int 非必填，授权云盘文件夹ID
        :param expiryTime: int时间戳, 非必填，课程有效期，默认空永久有效，
        :param mainTeacherUid: int非必填，班主任uid，默认空
        :param subjectId: int 课程学科分类
        :param allowAddFriend: int非必填，是否允许班级成员在群里互相添加好友，0=不允许，1=允许，传非0或非1报参数错误
        :param allowStudentModifyNickname:int非必填，是否允许学生在群里修改其班级昵称，0=不允许，1=允许，传非0或非1报参数错误，不传默认0
        :param notAllowDeleteCourseStudentReplay: string  是否不允许离开班级的学生或班级解散后，可查看课程内容 0=否（允许），1=是（不允许）
        :param courseUniqueIdentity: string非必填，机构可传唯一标识，传入此值后，我们会检验已创建课程中是否有该唯一标识
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'courseName': courseName,
            'folderId': folderId,
            'expiryTime': expiryTime,
            'mainTeacherUid': mainTeacherUid,
            'subjectId': subjectId,
            'allowAddFriend': allowAddFriend,
            'allowStudentModifyNickname': allowStudentModifyNickname,
            'notAllowDeleteCourseStudentReplay': notAllowDeleteCourseStudentReplay,
            'courseUniqueIdentity': courseUniqueIdentity,
        }

        response = requests.post(url=self.action.editCourse, data=payload).json()
        return response

    def end_course(self, courseId):
        """
        https://docs.eeo.cn/api/zh-hans/classroom/endCourse.html
        结束课程   注意：课程下没有正在上的课节，即可结束课程。
        如果课程下有尚未开始的课节，会删除未开始的课节之后结束课程，请谨慎使用此功能
        :param courseId:int 课程ID
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
        }
        response = requests.post(url=self.action.endCourse, data=payload).json()
        return response

    def add_course_class(self, courseId, className=None, beginTime=None, endTime=None, teacherUid=None,
                         seatNum=None, isHd=None, isDc=None, assistantUids=None, teachMode=None, isAutoOnstage=None,
                         record=None, recordScene=None, live=None, replay=None, watchByLogin=None,
                         allowUnloggedChat=None):
        """
        创建课节  具体可参考 https://docs.eeo.cn/api/zh-hans/classroom/addCourseClass.html
        :param courseId:int 课程ID
        :param className:
        :param beginTime:
        :param endTime:
        :param teacherUid:
        :param assistantUids: [] [123,456]
        :param seatNum: 上台人数
        :param isHd: 否	0=非高清，1=高清，2=全高清，默认为0，除了1和2，所有非0的数字,都会当成0处理	是否高清
        :param isDc: 双摄模式，是否开启副摄像头，0=不开启，3=开启全高清副摄像头,需要上台人数为1V1
        :param teachMode: 教学模式，1=在线教室，2=智慧教室	当teachMode=2时，isAutoOnstage会始终被设置为1
        :param isAutoOnstage:学生进入教室时是否自动上台 0=自动，1=不自动 所有非1的数字,都会当成0处理
        :param record:录课(0 关闭，1 开启)
        :param recordScene:录制现场(0 关闭，1 开启)
        :param live:直播(0 关闭，1 开启)
        :param replay:回放(0 关闭，1 开启)
        :param watchByLogin:只允许登录ClassIn账号后才可观看，未登录不可观看，0=未开启，1=开启	未开启录课、直播、回放中的两项及以上，此参数设置了也用不到
        :param allowUnloggedChat:允许未登录用户参与直播聊天和点赞，0=不允许，1=允许	未开启录课和直播，此参数设置了也用不到
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'className': className,
            'beginTime': beginTime,
            'endTime': endTime,
            'teacherUid': teacherUid,
            'assistantUids': assistantUids,
            'seatNum': seatNum,
            'isHd': isHd,
            'isDc': isDc,
            'teachMode': teachMode,
            'isAutoOnstage': isAutoOnstage,
            'record': record,
            'recordScene': recordScene,
            'live': live,
            'replay': replay,
            'watchByLogin': watchByLogin,
            'allowUnloggedChat': allowUnloggedChat,
        }
        if assistantUids is None:
            del payload['assistantUids']

        response = requests.post(url=self.action.addCourseClass, data=payload).json()
        return response

    def edit_course_class(self, courseId, classId, className=None, beginTime=None, endTime=None, teacherUid=None,
                          assistantUids=None, teachMode=None, isAutoOnstage=None, record=None, recordScene=None,
                          live=None, replay=None, watchByLogin=None, allowUnloggedChat=None):
        """

        编辑课节  https://docs.eeo.cn/api/zh-hans/classroom/editCourseClass.html
        :param courseId:int 课程ID
        :param classId:int 课节ID
        :param className:
        :param beginTime:
        :param endTime:
        :param teacherUid:
        :param assistantUids: [] [123,456]
        :param teachMode: 教学模式，1=在线教室，2=智慧教室	当teachMode=2时，isAutoOnstage会始终被设置为1
        :param isAutoOnstage:学生进入教室时是否自动上台 0=自动，1=不自动 所有非1的数字,都会当成0处理
        :param record:录课(0 关闭，1 开启)
        :param recordScene:录制现场(0 关闭，1 开启)
        :param live:直播(0 关闭，1 开启)
        :param replay:回放(0 关闭，1 开启)
        :param watchByLogin:只允许登录ClassIn账号后才可观看，未登录不可观看，0=未开启，1=开启	未开启录课、直播、回放中的两项及以上，此参数设置了也用不到
        :param allowUnloggedChat:允许未登录用户参与直播聊天和点赞，0=不允许，1=允许	未开启录课和直播，此参数设置了也用不到
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'classId': classId,
            'className': className,
            'beginTime': beginTime,
            'endTime': endTime,
            'teacherUid': teacherUid,
            'assistantUids': assistantUids,
            'teachMode': teachMode,
            'isAutoOnstage': isAutoOnstage,
            'record': record,
            'recordScene': recordScene,
            'live': live,
            'replay': replay,
            'watchByLogin': watchByLogin,
            'allowUnloggedChat': allowUnloggedChat,
        }

        response = requests.post(url=self.action.editCourseClass, data=payload).json()

        return response

    def del_course_class(self, courseId, classId):
        """
        删除课节  https://docs.eeo.cn/api/zh-hans/classroom/delCourseClass.html
        @param courseId:int 课程ID
        @param classId:int 课节ID
        @return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'classId': classId,
        }

        response = requests.post(url=self.action.delCourseClass, data=payload).json()

        return response

    def add_course_student(self, courseId, studentUid, identity=1):
        """
        添加课程学生  https://docs.eeo.cn/api/zh-hans/classroom/addCourseStudent.html
        :param courseId: int 课程ID
        :param studentUid: int 用户UID
        :param identity:int 默认为课程学生，学生和旁听的识别(1 为学生,2 为旁听)
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'studentUid': studentUid,
            'identity': identity
        }

        response = requests.post(url=self.action.addCourseStudent, data=payload).json()

        return response

    def add_course_student_multiple(self, courseId, user_list, identity=1):
        """
        批量添加课程学生 https://docs.eeo.cn/api/zh-hans/classroom/addCourseStudentMultiple.html
        :param courseId:int 课程ID
        :param user_list:[{'uid':123},{'uid':456}]
        :param identity:int 默认为课程学生，学生和旁听的识别(1 为学生,2 为旁听)
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'identity': identity,
            'studentJson': json.dumps(user_list)
        }

        response = requests.post(url=self.action.addCourseStudentMultiple, data=payload).json()

        return response

    def del_course_student(self, courseId, studentUid, identity=1):
        """
        删除课程学生    https://docs.eeo.cn/api/zh-hans/classroom/delCourseStudent.html
        :param courseId: int 课程ID
        :param studentUid:int 用户UID
        :param identity:int 默认为课程学生，学生和旁听的识别(1 为学生,2 为旁听)
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'identity': identity,
            'studentUid': studentUid
        }

        response = requests.post(url=self.action.delCourseStudent, data=payload).json()

        return response

    def del_course_student_multiple(self, courseId, user_list, identity):
        """
        批量删除课程学生    https://docs.eeo.cn/api/zh-hans/classroom/delCourseStudentMultiple.html
        :param courseId: int 课程ID
        :param user_list:['123', ..., '456']
        :param identity:int 默认为课程学生，学生和旁听的识别(1 为学生,2 为旁听)
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'identity': identity,
            'studentUidJson': json.dumps(user_list)
        }

        response = requests.post(url=self.action.delCourseStudentMultiple, data=payload).json()

        return response

    def add_class_student_multiple(self, courseId, classId, studentJson, identity=1):
        """
        课节批量添加学生 https://docs.eeo.cn/api/zh-hans/classroom/addClassStudentMultiple.html
        :param courseId:int 课程ID
        :param classId:
        :param identity:1
        :param studentJson:[{uid:123,name:xxxx}]
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'classId': classId,
            'identity': identity,
            'studentJson': json.dumps(studentJson)
        }

        response = requests.post(url=self.action.addClassStudentMultiple, data=payload).json()

        return response

    def del_class_student_multiple(self, courseId, classId, studentUidJson, identity=1):
        """
        课节批量删除学生 https://docs.eeo.cn/api/zh-hans/classroom/delClassStudentMultiple.html
        :param courseId:int 课程ID
        :param classId:
        :param studentUidJson:[123,456]
        :param identity:1
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'classId': classId,
            'identity': identity,
            'studentUidJson': json.dumps(studentUidJson)
        }

        response = requests.post(url=self.action.delClassStudentMultiple, data=payload).json()

        return response

    def modify_class_seatNum(self, courseId, classId, seatNum, isHd):
        """
        修改课节上台人数及清晰度  https://docs.eeo.cn/api/zh-hans/classroom/modifyClassSeatNum.html
        :param courseId: int 课程ID
        :param classId: int 课节ID
        :param seatNum: int 上台人数
        :param isHd: 是否高清(0=非高清，1=高清，2=全高清，非1的数字都会当做0来处理)
        :return:
        """
        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'classId': classId,
            'seatNum': seatNum,
            'isHd': isHd
        }

        response = requests.post(url=self.action.modifyClassSeatNum, data=payload).json()

        return response

    def modify_course_teacher(self, courseId, teacherUid):
        """
        更换课程老师 https://docs.eeo.cn/api/zh-hans/classroom/modifyCourseTeacher.html
        :param courseId:int 课程ID
        :param teacherUid:
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'teacherUid': teacherUid,
        }

        response = requests.post(url=self.action.modifyCourseTeacher, data=payload).json()

        return response

    def removeCourseTeacher(self, courseId, teacherUid):
        """
        移除课程老师 https://docs.eeo.cn/api/zh-hans/classroom/removeCourseTeacher.html
        :param courseId:int 课程ID
        :param teacherUid:
        :return:
        """

        timeStamp, safeKey = self.get_safe_key()
        payload = {
            'SID': self.SID,
            'timeStamp': timeStamp,
            'safeKey': safeKey,
            'courseId': courseId,
            'teacherUid': teacherUid,
        }

        response = requests.post(url=self.action.removeCourseTeacher, data=payload).json()

        return response

    """
    LMS  
    接口文档：https://docs.eeo.cn/api/zh-hans/LMS/
    验签规则：https://docs.eeo.cn/api/zh-hans/appendix/signature.html
    验签Demo：https://docs.eeo.cn/api/zh-hans/appendix/sign_demo.html
    --------------------------------------------------------------------------------------------------------------
    """

    def create_headers(self, payload):
        """
        创建验签所需信息
        :param payload: 需要签名的数据字典，其中不应包含列表、字典或长于1024个字符的字符串。
        :return:
        """
        sid = self.SID
        secret = self.secret
        timeStamp = int(time.time())

        # 过滤掉列表、字典或过长的字符串和数值
        filtered_data = {k: v for k, v in payload.items() if not isinstance(v, (list, dict)) and len(str(v)) <= 1024}
        filtered_data['sid'] = sid
        filtered_data['timeStamp'] = timeStamp

        sorted_items = sorted(filtered_data.items())  # 将字典项排序
        sign_string = "&".join(f"{key}={value}" for key, value in sorted_items)  # 构建用于签名的字符串

        # 拼接签名密钥
        sign_string += "&key={}".format(secret)
        sign = hashlib.md5(sign_string.encode('utf-8')).hexdigest()

        headers = {
            'X-EEO-SIGN': sign,
            'X-EEO-UID': f'{sid}',
            'X-EEO-TS': f'{timeStamp}',
            'Content-Type': 'application/json'
        }
        return headers

    def create_unit(self, courseId: int, unitName: str, content: str, publishFlag: int):
        """
        创建LMS单元
        :param courseId: 课程ID
        :param unitName:单元名称-50字符，超出截断
        :param content:单元描述
        :param publishFlag: 发布状态 0,草稿;1隐藏,2显示
        :return:
        """

        payload = {
            'courseId': courseId,
            'name': unitName,
            'content': content,
            'publishFlag': publishFlag  # 发布状态 0,草稿;1隐藏,2显示
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/unit/create'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        return response

    def update_unit(self, courseId: int, unitId: int, unitName: str, content: str, publishFlag: int):
        """
        编辑单元信息
        :param courseId: 课程ID
        :param unitId: 单元ID
        :param unitName:单元名称-50字符，超出截断
        :param content:单元描述
        :param publishFlag: 发布状态 0,草稿;1隐藏,2显示
        :return:
        """

        payload = {
            'courseId': courseId,
            'unitId': unitId,
            'name': unitName,
            'content': content,
            'publishFlag': publishFlag
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/unit/update'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        return response

    def delete_unit(self, courseId: int, unitId: int):
        """
        删除单元
        :param courseId: 课程ID
        :param unitId: 单元ID
        :return:
        """

        payload = {
            'courseId': courseId,
            'unitId': unitId,
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/unit/delete'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        return response

    def move_unit(self, courseId: int, unitId: int, toUnitId: int):
        """
        移动单元下活动
        :param courseId: 课程ID
        :param unitId: 单元ID
        :param toUnitId:
        :return:
        """
        payload = {
            'courseId': courseId,
            'unitId': unitId,
            'toUnitId': toUnitId,
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/unit/move'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        return response

    def release_activity(self, courseId: int, activityId: int):
        """
        发布活动
        :param courseId: 课程ID
        :param activityId:
        :return:
        """
        payload = {
            'courseId': courseId,
            'activityId': activityId,
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/activity/release'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        return response

    def delete_activity(self, courseId: int, activityId: int):
        """
        删除活动
        :param courseId: 课程ID
        :param activityId:
        :return:
        """
        payload = {
            'courseId': courseId,
            'activityId': activityId,
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/activity/delete'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        return response

    def add_activity_student(self, courseId: int, activityId: int, studentUids: list):
        payload = {
            'courseId': courseId,
            'activityId': activityId,
            'studentUids': studentUids,
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/activity/addStudent'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        return response

    def delete_activity_student(self, courseId: int, activityId: int, studentUids: list):
        payload = {
            'courseId': courseId,
            'activityId': activityId,
            'studentUids': studentUids,
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/activity/deleteStudent'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        return response

    def create_lms_lesson(self, courseId, unitId, lessonName=None, teacherUid=None, assistantUids=None, 
                          startTime=None, endTime=None, seatNum=None, isHd=None, cameraHide=None, isAutoOnstage=None, 
                          liveState=None, openState=None, recordState=None, recordType=None, isAllowCheck=None, 
                          uniqueIdentity=None):
        payload = {
            'courseId': courseId,
            'unitId': unitId,
            'name': lessonName,
            'teacherUid': teacherUid,
            'assistantUids': assistantUids,  # 示例：[1000082,1000083]
            'startTime': startTime,
            'endTime': endTime,
            'seatNum': seatNum,  # 上台人数，默认1V6 和原API逻辑不一致5=1V4
            'isHd': isHd,  # 0 = 非高清，1 = 高清，2 = 全高清。默认为0，不传使用默认值，传错报 参数错误。目前仅支持 1V1 或 1V6 高清、全高清
            'cameraHide': cameraHide,  # 是否隐藏坐席区，0 = 否（显示坐席区），1= 是（隐藏坐席区）
            'isAutoOnstage': isAutoOnstage,  # 0 = 不自动，1 = 自动。
            'liveState': liveState,  # 是否直播 0 不直播 1 直播
            'openState': openState,  # 是否公开回放 0 不公开 1 公开
            'recordState': recordState,  # 是否录课 0 不录课， 1 录课
            'recordType': recordType,  # 录课类型 0 录教室 1 录老师 2 两个都录
            'isAllowCheck': isAllowCheck,  # 是否允许互相查看学习报告和评分，0=不允许 1=允许
            'uniqueIdentity': uniqueIdentity
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/activity/createClass'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        
        return response

    def update_lms_lesson(self, courseId, unitId, activityId, lessonName=None, teacherUid=None, assistantUids=None, 
                          startTime=None, endTime=None, seatNum=None, isHd=None, cameraHide=None, isAutoOnstage=None, 
                          liveState=None, openState=None, recordState=None, recordType=None, isAllowCheck=None, 
                          uniqueIdentity=None):

        payload = {
            'courseId': courseId,
            'unitId': unitId,
            'activityId': activityId,
            'name': lessonName,
            'teacherUid': teacherUid,
            'assistantUids': assistantUids,  # 示例：[1000082,1000083]
            'startTime': startTime,
            'endTime': endTime,
            'seatNum': seatNum,   # 上台人数，默认1V6 和原API逻辑不一致5=1V4
            'isHd': isHd,  # 0 = 非高清，1 = 高清，2 = 全高清。默认为0，不传使用默认值，传错报 参数错误。目前仅支持 1V1 或 1V6 高清、全高清
            'isAutoOnstage': isAutoOnstage,
            'liveState': liveState,  # 是否直播 0 不直播 1 直播
            'openState': openState,  # 是否公开回放 0 不公开 1 公开
            'recordState': recordState,  # 是否录课 0 不录课， 1 录课
            'recordType': recordType,  # 录课类型 0 录教室 1 录老师 2 两个都录
            'cameraHide': cameraHide,  # 是否隐藏坐席区，0 = 否（显示坐席区），1= 是（隐藏坐席区）
            'isAllowCheck': isAllowCheck,  # 是否允许互相查看学习报告和评分，0=不允许 1=允许
            'uniqueIdentity': uniqueIdentity  # 唯一标识
        }
        sign_headers = self.create_headers(payload)  # 签名信息
        path = '/lms/activity/updateClass'
        target_url = domain + path
        response = requests.post(url=target_url, data=json.dumps(payload), headers=sign_headers).json()
        return response
