import sqlite3
    

def add_job(author_id:int, type:str, about:str, description:str, compensation:str, thread_link:str):
  try:
    conn = sqlite3.connect('jobs_and_opportunities.db')
    cursor = conn.cursor()
    cursor.execute(
      "INSERT INTO created_jobs VALUES(:author_id, :type, :about, :description, :compensation, :thread_link)",
      {
        "author_id": author_id,
        "type": type,
        "about": about,
        "description": description,
        "compensation": compensation,
        "thread_link": thread_link
      })
    conn.commit()
    conn.close()
    print('added in database : ',about)
  except Exception as e:
      print(e)

    
def get_jobs(query):
  try:
    conn = sqlite3.connect('jobs_and_opportunities.db')
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT about,compensation,thread_link FROM created_jobs WHERE {query}"
      )
    a=cursor.fetchall()
    conn.close()
    print(a)
    return (a if len(a)>0 else 400)
  except Exception as e:
    print(e)

conn = sqlite3.connect('jobs_and_opportunities.db')
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS created_jobs(
        author_id INT,
        type TEXT,
        about TEXT,
        description TEXT,
        compensation TEXT,
        thread_link TEXT
)
""")
conn.commit()
conn.close()




"""add_job(123, "backend", "asldjfhjkh dfkjasdhf kja", "askdjfhkjasd fhkasjdfhjk0","paid","https://google.com")
add_job(121, "backend", "asldjfhjkh dfkjasdhf kja", "askdjfhkjasd fhkasjdfhjk0","unpaid","https://google.com")
add_job(124, "backend", "asldjfhjkh dfkjasdhf kja", "askdjfhkjasd fhkasjdfhjk0","paid","https://google.com")
add_job(125, "frontend", "asldjfhjkh dfkjasdhf kja", "askdjfhkjasd fhkasjdfhjk0","paid","https://google.com")
add_job(126, "frontend", "asldjfhjkh dfkjasdhf kja", "askdjfhkjasd fhkasjdfhjk0","internship","https://google.com")
print('added all')
print('searching...')
"""

"""print(get_jobs("type = 'frontend' AND compensation IN ('internship')"))"""
  




