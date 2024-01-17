from .base import Base

class Resume(Base):
    def test_resume(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tadey Pyliachyk', response.data)

    def test_page2(self):
        response = self.client.get('/page2', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Highlander', response.data)  

    def test_page3(self):
        response = self.client.get('/page3', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tadey Pyliachyk, Ivano-Frankivsk, 2023', response.data)  