# 🎨 Automated Trivia Poster & Media Generator

A Python-based automation tool designed to streamline the creation of promotional graphics and winner announcements for weekly trivia events. By eliminating manual photo-editing, this application dynamically composites raw event photos, branded logos, and advanced typography into publish-ready social media assets.

## ✨ Features
* **Automated Image Compositing:** Automatically calculates aspect ratios and precisely overlays branded logos and rank medals (1st, 2nd, 3rd) onto png photos.
* **Advanced Typography Engine:** Utilizes `Pillow (PIL)` to render complex, multi-layered text effects. Features include:
  * Programmatic metallic text gradients (Gold, Silver, Bronze).
  * Dynamic drop-shadows and Gaussian blur glows based on font size and rank.
* **One-Click Poster Generation:** Takes a base poster template and precisely overlays gradient edition numbers and winning team names using pre-calculated layouts.
* **Lightweight GUI:** Built with `Tkinter` to provide a fast, distraction-free data entry window for inputting the Edition number and Top 3 teams right at the venue.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **GUI Framework:** Tkinter (Standard Library)
* **Image Processing:** Pillow (PIL)
* **File Management:** OS & Sys modules

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/PotraVVlad/WinnersPicturesEditor.git](https://github.com/PotraVVlad/WinnersPicturesEditor.git)
