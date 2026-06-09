# נוהל גיבויים – Railway (Pro)

גיבוי מסד הנתונים וקבצי המדיה של הפרויקט `tvunat-hameaver` ב-Railway.

## מה מגבים

| מה | שירות | Volume | Mount |
|----|-------|--------|-------|
| מסד הנתונים (PostgreSQL) | `Postgres` | `postgres-volume` | `/var/lib/postgresql/data` |
| קבצי מדיה שהועלו | `web` | `web-volume` | `/data` (`MEDIA_ROOT`) |

---

## חלק א: גיבוי מתוזמן פנימי (עיקרי) – הגדרה ב-UI של Railway

פעולות אלו מתבצעות בלוח הבקרה של Railway (אי אפשר דרך קוד):

1. שירות `Postgres` ← טאב `Backups` ← להפעיל לוח זמנים `Daily` + `Weekly`.
2. שירות `web` ← טאב `Backups` ← להפעיל לוח זמנים `Daily` + `Weekly` עבור `web-volume`.
3. ללחוץ `Backup` ידני אחד מיד אחרי ההפעלה, ולוודא שמופיע גיבוי ברשימה.

שמירה (ברירת מחדל של Railway): יומי נשמר 6 ימים, שבועי כחודש, חודשי כ-3 חודשים.

---

## חלק ב: נוהל גיבוי ידני לפני שינוי מסוכן

לפני deploy גדול, מיגרציה כבדה/שינוי סכימה, או שינוי תשתית:

1. שירות `Postgres` ← טאב `Backups` ← `Backup` (ידני, מיידי).
2. אם השינוי נוגע גם למדיה: שירות `web` ← טאב `Backups` ← `Backup`.

מגבלה: גיבוי ידני מוגבל ל-50% מגודל ה-volume.

---

## חלק ג: גיבוי חיצוני קל של ה-DB (הגנה מאובדן מוחלט)

מגן מפני מחיקת volume/פרויקט ששוברת את הגיבויים הפנימיים. ממומש כ-GitHub Action
מתוזמן (שבועי) ב-[.github/workflows/db-backup.yml](.github/workflows/db-backup.yml)
שמריץ `pg_dump` מול הפרוקסי הציבורי של Railway ושומר את הקובץ כ-artifact.

### הגדרה חד-פעמית

1. ב-Railway: שירות `Postgres` ← טאב `Variables` ← להעתיק את הערך של `DATABASE_PUBLIC_URL`.
2. ב-GitHub: `Settings` ← `Secrets and variables` ← `Actions` ← `New repository secret`:
   - שם: `DATABASE_PUBLIC_URL`
   - ערך: הערך שהעתקת.
3. ה-Action ירוץ אוטומטית כל שבוע, או ידנית דרך `Actions` ← `Weekly DB Backup` ← `Run workflow`.

### היכן נשמר הגיבוי

artifact בשם `db-backup` תחת ה-run ב-GitHub Actions, נשמר 30 יום. להורדה: לפתוח את
ה-run הרלוונטי ולהוריד את ה-artifact.

> היקף: מסד הנתונים בלבד. קבצי המדיה מגובים בגיבוי הפנימי (חלקים א/ב).

---

## חלק ד: נוהל שחזור

### שחזור פנימי (Railway)

1. שירות `Postgres` (או `web` למדיה) ← טאב `Backups`.
2. בחירת גיבוי לפי תאריך ← `Restore` ← סקירה ב-`Details` ← `Deploy`.

> אזהרה: שחזור משחזר לאותו project+environment ומוחק גיבויים חדשים יותר מנקודת השחזור.

### שחזור חיצוני (מ-artifact של pg_dump)

```bash
# יעד: DB ריק/חדש; משתמשים בכתובת הפרוקסי הציבורי
pg_restore --no-owner --clean --if-exists -d "NEW_DATABASE_PUBLIC_URL" hanit-yoga-YYYYMMDD-HHMMSS.dump
```

---

## הערות

- עלות: גיבויים מחויבים לפי נפח אינקרמנטלי (~$0.15/GB/חודש), בדרך כלל זניח לפרויקט בגודל הזה.
- אבטחה: מומלץ לבצע rotate לסיסמת ה-DB ול-`DJANGO_SECRET_KEY` מעת לעת, ובמיוחד אם נחשפו.
