
<h3 align="center">🖼️ Browser Hidden ChatGPT (Anti-Screen Capture PoC)</h3>


<p align="center">
  A stealthy, frameless ChatGPT browser using PyQt6 and Windows API to demonstrate how to hide windows from screen capture tools — for educational use only.
</p>
---

## 📚 About This Project

This project is a **proof-of-concept (PoC)** for educational and awareness purposes.

It demonstrates how the Windows API [`SetWindowDisplayAffinity`](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowdisplayaffinity) can be used to hide a window from screen recording and screenshot tools.

---

## 🔍 tools

Inspired by tools like [InterviewCoder](https://www.interviewcoder.co/) ([see article](https://www.cnbc.com/2025/03/09/google-ai-interview-coder-cheat.html)), this project shows how simple techniques can bypass screen sharing detection.

By applying `WDA_EXCLUDEFROMCAPTURE`, a window's content will be hidden from screen recorders and remote viewers — meaning interviewers may not see what the user is actually doing.

---

## 🔧 Features

- ✅ Simple PyQt6-based browser loading [ChatGPT](https://chatgpt.com/)
- ✅ Frameless and always-on-top window
- ✅ Keyboard shortcuts to hide/restore window opacity
- ✅ `SetWindowDisplayAffinity` to hide window from screen captures
- ✅ Draggable border with styled UI

---
## Pip
<pre>
pip install PyQt6 PyQt6-WebEngine
</pre>

<h3>Example 1: Link Removal in Office Document</h3>
<img src="https://github.com/idanless/sanitize-pdf-and-office/blob/main/CDRIMG/remove%20link.jpeg?raw=true" alt="Example 1">

