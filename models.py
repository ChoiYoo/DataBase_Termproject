from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 회원 정보
class UserData(db.Model):  # UserData 모델 선언
    __tablename__ = 'userdata'  # 테이블 이름 지정
    # 각 Column 선언
    # 여기서 기본 키는 userNum이고 데이터가 저장되면 autoincrement=True를 통해 자동으로 번호가 매겨짐
    userNum = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 회원번호
    userId = db.Column(db.String(32))  # 회원ID
    userPw = db.Column(db.String(255))  # 회원PW
    userMajor = db.Column(db.String(32))  # 회원의 전공
    userLang = db.Column(db.String(32))  # 회원의 특기언어

    # db.relationship을 사용해 관계설정 (실제 데이터필드에 나타나는게 아닌 가상 필드, backref는 가상 필드 이름)

    # UserData와 ConditionData는 1:N관계
    # 조건선택을 하면 조건 선택한 회원을 `conditiondata.user`을 이용해 접근할 수 있음
    conditiondatas = db.relationship('ConditionData', backref='user')
    # UserData와 DoneTeamData는 1:N관계
    # 팀 합류를 하면 팀에 합류한 회원을 `doneteamdata.user`을 이용해 접근할 수 있음
    doneteamdatas = db.relationship('DoneTeamData', backref='userid')

# 팀의 정보
class WaitTeamData(db.Model):  # WaitTeamData 모델 선언
    __tablename__ = 'waitteamdata'  # 테이블 이름 지정
    # 각 Column 선언
    # 여기서 기본 키는 teamCode이고 데이터가 저장되면 autoincrement=True를 통해 자동으로 번호가 매겨짐
    teamCode = db.Column(db.Integer, primary_key = True, autoincrement=True)  # 팀번호
    teamName = db.Column(db.String(32))  # 팀이름
    teamIntro = db.Column(db.String(128))  # 팀에 대한 소개글
    teamTo = db.Column(db.String(32))  # 팀의 여행 목적지
    teamRecNum = db.Column(db.Integer)  # 팀에 현재 합류되어 있는 회원 수
    teamNumGoal = db.Column(db.Integer)  # 팀의 목표 인원

    # db.relationship을 사용해 관계설정 (실제 데이터필드에 나타나는게 아닌 가상 필드, backref는 가상 필드 이름)

    # WaitTeamData와 DoneTeamData는 1:N관계
    # 팀 합류를 하면 합류한 팀을 `doneteamdata.teamcode`를 이용해 접근할 수 있음
    doneteamdatas= db.relationship('DoneTeamData', backref='teamcode', lazy=True)
    # ContactDat와 WaitTeamData는 1:1관계 (그러므로 uselist=False)
    # 팀 생성을 하면 주소에 대한 팀을 `contactdata.teamcode`를 이용해 접근할 수 있음
    contactdatas = db.relationship('ContactData', backref='teamcode', uselist=False)

# 매칭된 팀과 회원, 합류한 팀에 대한 회원의 만족 여부
class DoneTeamData(db.Model):  # DoneTeamData 모델 선언
    __tablename__ = 'doneteamdata'  # 테이블 이름 지정
    # 각 Column 선언
    # 여기서 기본 키는 id이고 데이터가 저장되면 autoincrement=True를 통해 자동으로 번호가 매겨짐
    # teamCode는 WaitTeamData 모델의 teamCode 참조
    # userNum은 UserData 모델의 userNum 참조
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teamCode = db.Column(db.Integer, db.ForeignKey('waitteamdata.teamCode'))  # waitteamdata에 저장되어 있는 팀 중 회원이 합류한 팀번호
    userNum = db.Column(db.Integer, db.ForeignKey('userdata.userNum'))  # userdata에 저장되어 있는 회원번호
    userSat = db.Column(db.String(32))  # 회원의 합류한 팀에 대한 만족 여부

# 팀의 연락 수단
class ContactData(db.Model):  # ContactData 모델 선언
    __tablename__ = 'contactdata'  # 테이블 이름 지정
    # 각 Column 선언
    # 여기서 기본 키는 id이고 데이터가 저장되면 autoincrement=True를 통해 자동으로 번호가 매겨짐
    # teamCode는 WaitTeamData 모델의 teamCode 참조
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teamCode = db.Column(db.Integer, db.ForeignKey('waitteamdata.teamCode'))  # waitteamdata에 저장되어 있는 팀번호
    teamAddress = db.Column(db.String(128))  # 팀주소

# 나라 정보
class NeedLangData(db.Model):  # NeedLangData 모델 선언
    __tablename__ = 'needlangdata'  # 테이블 이름 지정
    # 각 Column 선언
    # 여기서 기본 키는 countryCode이고 데이터가 저장되면 autoincrement=True를 통해 자동으로 번호가 매겨짐
    countryName = db.Column(db.String(32))  # 나라 이름
    countryCode = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 나라 번호
    countryLang = db.Column(db.String(32))  # 나라 사용 언어

# 회원이 선택한 조건 정보
class ConditionData(db.Model):  # ConditionData 모델 선언
    __tablename__ = 'conditiondata'  # 테이블 이름 지정
    # 각 Column 선언
    # 여기서 기본 키는 id이고 데이터가 저장되면 autoincrement=True를 통해 자동으로 번호가 매겨짐
    # userNum은 UserData 모델의 userNum 참조
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userNum = db.Column(db.Integer, db.ForeignKey('userdata.userNum'))  # userdata에 저장되어 있는 회원 번호
    travelDes = db.Column(db.String(32))  # 회원이 원하는 여행목적지
    travelNum = db.Column(db.Integer)  # 회원이 원하는 팀의 목표 인원
    travelLang = db.Column(db.String(32))  # 회원의 특기 언어