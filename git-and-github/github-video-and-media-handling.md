# GitHub Video and Media Handling

**Date:** 2024-12-05  
**Category:** Git & GitHub

## Problem
Tried to upload a 4MB video to GitHub repo, but the web interface showed:
```
(Sorry about that, but we can't show files that are this big right now.)
```

Even though the file was under GitHub's 100MB limit, videos don't display inline on GitHub.

---

## Solutions Discovered

### 1. **GitHub Video Limitations**
- GitHub **accepts videos up to 100MB** in repos
- Web UI **won't display videos inline** (even small ones)
- Shows "can't show files this big" message for any video

### 2. **Best Practices for Videos in GitHub**

#### Option A: Direct Download Link (Simplest)
```markdown
[📹 Download Demo Video](https://github.com/username/repo/raw/main/assets/demo.mp4)
```

**Pros:** Simple, no extra tools needed  
**Cons:** Requires download to watch

---

#### Option B: Convert to GIF (Best for README)
```bash
# Using online tool: https://ezgif.com/video-to-gif
# Settings:
# - Width: 800px
# - Frame rate: 10 FPS
# - Method: Lanczos3
```

Or with ffmpeg:
```bash
sudo apt install ffmpeg

ffmpeg -i demo.mp4 -vf "fps=10,scale=800:-1:flags=lanczos" \
  -loop 0 demo.gif
```

**In README:**
```markdown
![Demo](assets/demo.gif)
```

**Pros:** Plays inline, great UX  
**Cons:** Larger file size, lower quality

---

#### Option C: YouTube + Thumbnail (Most Professional)
1. Upload to YouTube as **Unlisted**
2. Get video ID from URL
3. Use in README:
```markdown
[![Watch Demo](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://youtu.be/VIDEO_ID)
```

**Pros:** No size limits, SEO benefits, professional  
**Cons:** Requires YouTube account

---

#### Option D: GitHub Releases (For Large Files)
1. Go to repo → Releases → Create new release
2. Upload video as release asset (up to 2GB)
3. Link in README:
```markdown
[📹 Watch Demo](https://github.com/user/repo/releases/download/v1.0/demo.mp4)
```

**Pros:** Doesn't bloat repo size, supports large files  
**Cons:** Extra step, not version controlled

---

### 3. **Recommended Approach**

Use **both GIF + video link** for best UX:
```markdown
## 🎥 Demo

![Quick Preview](assets/demo.gif)

**[📹 Watch Full Quality Demo (4MB)](https://github.com/user/repo/raw/main/assets/demo.mp4)**
```

**Why this works:**
- GIF plays inline → instant engagement
- Video link available → full quality option
- No external dependencies

---

### 4. **File Size Best Practices**

| File Type | Recommended Size | Max Size |
|-----------|------------------|----------|
| GIF | < 5MB | 10MB |
| Video (in repo) | < 25MB | 100MB |
| Video (releases) | < 100MB | 2GB |
| Images | < 1MB | 10MB |

**Optimization Tips:**
```bash
# Compress video
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4

# Optimize GIF
ffmpeg -i input.mp4 -vf "fps=10,scale=800:-1:flags=lanczos" output.gif
```

---

## Key Takeaways

✅ GitHub accepts videos but won't display them inline  
✅ GIFs provide the best inline experience for READMEs  
✅ Combine GIF preview + video download link for optimal UX  
✅ Use GitHub Releases for videos > 25MB  
✅ Always optimize media files before uploading  

---

## Resources

- [GitHub File Limits](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)
- [ezgif.com](https://ezgif.com/video-to-gif) - Online video to GIF converter
- [ffmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Git LFS](https://git-lfs.github.com/) - For version controlling large files

---

## Tags
`github` `git` `video` `gif` `media` `optimization` `readme` `documentation`