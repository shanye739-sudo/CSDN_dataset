import sqlite3
import os


class CSDNDBViewer:
    """
    A simple viewer for CSDN SQLite dataset.
    Designed for GitHub users to easily read and inspect .db files.
    """

    def __init__(self, db_name="csdn_2021_ultra_200.db"):
        self.db_name = db_name

        # 检查文件是否存在
        if not os.path.exists(self.db_name):
            raise FileNotFoundError(f"❌ 找不到数据库文件: {self.db_name}")

    def connect(self):
        """建立数据库连接"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def show_schema(self):
        """查看表结构"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        return [t[0] for t in tables]

    def load_all(self):
        """读取全部数据"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, pub_time, url, likes, comments, favorites, views, content
            FROM articles
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows

    def sample(self, n=5):
        """查看前n条数据（快速预览）"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, pub_time, url, likes, comments, favorites, views, content
            FROM articles
            LIMIT ?
        """, (n,))

        rows = cursor.fetchall()
        conn.close()
        return rows

    def pretty_print(self, n=3):
        """格式化打印数据（类似你原来的版本）"""
        rows = self.sample(n)

        if not rows:
            print("⚠️ 数据为空")
            return

        print(f"\n✅ 数据预览（显示 {len(rows)} 条）\n")
        print("=" * 80)

        for i, row in enumerate(rows, 1):
            content_snippet = (row["content"] or "")[:80].replace("\n", " ").strip()

            print(f"【文章 {i}】")
            print(f"📌 标题: {row['title']}")
            print(f"⏰ 时间: {row['pub_time']}")
            print(f"🔗 链接: {row['url']}")
            print(f"👍 赞: {row['likes']} | 💬 评论: {row['comments']} | ⭐ 收藏: {row['favorites']} | 👁️ 浏览: {row['views']}")
            print(f"📝 摘要: {content_snippet}...")
            print("-" * 80)
