# Run this within the virtualenv, after activating the virtualenv

def setUpSession():
    config = 'development.ini'
    from pyramid.paster import get_appsettings
    settings = get_appsettings(config)
    from sqlalchemy import engine_from_config
    engine = engine_from_config(settings, 'sqlalchemy.')
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    from learning_journal.models import MyModel
    session.query(MyModel).all()

def createNewEntryRows():
    entryObjList = []
    for subject, desc in [('A Beautiful Mind', 'Russell Crowe plays the scientist'), ('Dead Poets society', 'Robin Williams did a class act, went above and beyond his duties'), ('The Theory of Everything', 'grand quest of Albert Einstein')]:
        entryObjList.append(Entry(title=subject, body=desc))
    
    session.add_all(entryObjList)
    session.entryObjList
    session.commit()

def queryTableById():
    for obj in session.query(Entry).filter(Entry.id = id):
        print obj.title, obj.body

def queryTableAndOrder():
    for obj in session.query(Entry).all().order_by(Entry.created):
        print obj.title, obj.body

setupSession()
createNewEntryRows()
quertTableById(1)
queryTableAndOrder()




