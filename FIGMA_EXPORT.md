# הורדת לוגו ותמונות מפיגמה

כדי להכניס את הלוגו והתמונות האמיתיות מהעיצוב (במקום ה-placeholders):

1. **קבלת טוקן גישה מפיגמה**
   - היכנסי ל-[Figma](https://www.figma.com) → **Settings** (פרופיל) → **Security** → **Personal access tokens**
   - צרי טוקן חדש (וודאי שיש scope לקריאת קבצים)

2. **שמירת הטוקן לפיתוח**
   - פתחי את הקובץ `.env` בשורש הפרויקט והדביקי את הטוקן אחרי `FIGMA_ACCESS_TOKEN=`:
   ```
   FIGMA_ACCESS_TOKEN=figd_xxxxxxxx...
   ```
   - הקובץ `.env` לא נשמר ב-Git (מטעמי אבטחה).

3. **הרצת הפקודה מהפרויקט**
   ```bash
   cd c:\hanit-yoga
   .\.venv\Scripts\python manage.py figma_export_images
   ```
   (הפקודה קוראת את הטוקן מ-`.env` או ממשתנה הסביבה.)
   או עם טוקן מפורש:
   ```bash
   .\.venv\Scripts\python manage.py figma_export_images --token=הטוקן_שלך
   ```

4. **תוצאה**
   - הקבצים `logo.png`, `hero-banner.png` (ואם רלוונטי `header.png`) יישמרו ב-`yoga/static/yoga/images/`
   - האתר ישתמש בהם אוטומטית בדף הבית (אם לא הועלו תמונות דרך האדמין)

5. **באנר רקע בלבד (בלי קופסה וטקסט)**
   - כדי להוריד רק את תמונת הרקע של ה-Hero (בלי השכבות של הטקסט והקופסה הלבנה):
   ```bash
   .\.venv\Scripts\python manage.py figma_export_images --hero-background-only
   ```
   (אם הטוקן ב-`.env`, אין צורך ב-`--token`.)
   - הפקודה מחפשת את השכבה התחתונה (רקע) בתוך פריים ה-HERO BANNER ומייצאת רק אותה ל-`hero-banner.png`.

**הערה:** קובץ הפיגמה והצמתים (node IDs) מקושרים ל-PROJECT-1 (הדר + באנר דסקטופ). אם העיצוב השתנה, ייתכן שיהיה צורך לעדכן את המזהים ב-`yoga/management/commands/figma_export_images.py`.
