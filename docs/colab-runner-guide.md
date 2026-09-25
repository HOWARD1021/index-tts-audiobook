# Google Colab CUDA 有聲書生成指南

本指南說明如何使用 Google Colab GPU (CUDA) 環境執行 IndexTTS-2.5 有聲書章節生成，消除本機 Apple Silicon (MPS) 在長時生成時的記憶體與 swap 負擔，並透過 Google Drive 進行斷點續傳與自動歸檔。

---

## 一、本地檔案位置清單 (Local File Inventory)

在開始使用 Colab 之前，你本機既有的有聲書專案資產位於以下路徑：

### 1. 聲音參考音檔 (Speaker Reference Voice)
- **選定發音人**：圓圓 (Yuanyuan)
- **音檔絕對路徑**：
  - 主要路徑：`/Users/howard/index-tts-workspace/index-tts/prompts/voice.wav`
  - 備份路徑：`/Users/howard/index-tts-workspace/index-tts/prompts/yuanyuan/yuanyuan_vocals_30s.wav`
- **音訊格式**：Mono PCM 16-bit, 22,050 Hz (約 30 秒人聲純音軌)
- **SHA-256 驗證碼**：`d8ba82bf2f84c2c0ff0ea03d8f9f2fcfef2ac0592a384381a4415fd8f53d71b7`

### 2. 章節腳本文稿 (13 Chapters Narration Scripts)
- **目錄路徑**：  
  `/Users/howard/Downloads/幽靈的禮物/volume-price-analysis-en-chapters/zh-simplified-tts/scripts/`
- **章節清單**：
  - `00-foreword-zh-simplified.md`
  - `01-chapter-one-zh-simplified.md`
  - `02-chapter-two-zh-simplified.md`
  - `03-chapter-three-zh-simplified.md`
  - `04-chapter-four-zh-simplified.md`
  - `05-chapter-five-zh-simplified.md`
  - `06-chapter-six-zh-simplified.md`
  - `07-chapter-seven-zh-simplified.md`
  - `08-chapter-eight-zh-simplified.md`
  - `09-chapter-nine-zh-simplified.md`
  - `10-chapter-ten-zh-simplified.md`
  - `11-chapter-eleven-zh-simplified.md`
  - `12-chapter-twelve-zh-simplified.md`

### 3. 本地成品與發布腳本
- **本地音訊存放目錄**：  
  `/Users/howard/Downloads/幽靈的禮物/volume-price-analysis-en-chapters/zh-simplified-tts/audio/`
- **Cloudflare R2 / Podcast 發布腳本**：  
  `/Users/howard/Downloads/幽靈的禮物/volume-price-analysis-en-chapters/zh-simplified-tts/publish_podcast.py`
- **R2 Bucket**：`howard-audiobooks`
- **公開 Feed URL**：`https://pub-43dc4106670549999990fa09d26d8316.r2.dev/feed.xml`

---

## 二、Google Drive 目錄架構

Colab 運行時會自動掛載 Google Drive，並以 `audiobook-workspace` 為根目錄：

```text
Google Drive: 我的雲端硬碟/
└── audiobook-workspace/
    ├── checkpoints/
    │   └── IndexTTS-2/          # 模型權重 (初次執行時自動由 Hugging Face 下載，約 4~6 GB)
    ├── prompts/
    │   └── voice.wav            # 請將本機 voice.wav 上傳至此
    ├── scripts/
    │   ├── 00-foreword.md       # 請將章節 Markdown 文稿上傳至此
    │   ├── 01-chapter-one.md
    │   └── ...
    ├── output/                  # 生成結果（包含章節完整 WAV、manifest 與每段 chunk）
    │   ├── 00-foreword.wav
    │   ├── 00-foreword.manifest.json
    │   └── 00-foreword.chunks/
    └── config/
        └── colab-cuda.toml      # CUDA 生成設定檔 (Notebook 會自動建立)
```

---

## 三、Colab 操作步驟

### 步驟 1：開啟 Notebook
1. 瀏覽器前往 [Google Colab](https://colab.research.google.com/)。
2. 選擇 **GitHub** 分頁，輸入專案網址或組織名稱：`HOWARD1021/index-tts-audiobook`。
3. 點選開啟 **`notebooks/colab_indextts_render.ipynb`**。

### 步驟 2：切換至 GPU 執行階段
1. 點擊頂部選單 **執行階段 (Runtime) ➔ 變更執行階段類型 (Change runtime type)**。
2. 硬體加速器選擇 **T4 GPU**（Colab 免費版即可）或 **L4 / A100**（Colab Pro）。
3. 儲存設定。

### 步驟 3：依序執行 Notebook 單元格
1. **單元格 1~2（硬體與 Drive 掛載）**：確認 GPU 正常並授權掛載 Google Drive。
2. **單元格 3（安裝環境）**：自動 clone IndexTTS 核心程式並安裝 `index-tts-audiobook[indextts]`，包含 IndexTTS-2.5 初始化必需的日文 G2P 套件 `fugashi` 與 `unidic-lite`。若遇到 `No module named 'fugashi'`，請同步最新 notebook 並重新執行此安裝單元格後再生成。
3. **單元格 4（下載模型）**：
   - 若 Drive 中已有權重，直接跳過；
   - 若無，會自動從 Hugging Face 下載 `IndexTeam/IndexTTS-2.5` 權重至 Drive。
4. **單元格 5~6（設定與文稿檢查）**：建立 `colab-cuda.toml` 並確認 prompts 與 scripts 目錄中是否有檔案。

### 步驟 4：執行生成
- **單章測試（Step 8）**：生成特定章節（預設為範例或指定的某章）。
- **全書 13 章批次自動生成（Step 10）**：
  直接執行 Step 10 的批次單元格，它會循序處理 `scripts/` 底下的所有 Markdown 檔，自動完成段落切分、GPU 生成、格式檢驗與 WAV 合併。

---

## 四、斷線與中斷保護機制 (Resume Safety)

- **分段檢查點**：管線是以 300~400 字為一個 chunk 進行生成，每完成一個 chunk 就會立即寫入磁碟並更新 SHA-256 manifest。
- **免重複生成**：若遇到 Colab 閒置斷線或網路中斷，**重新連線後直接再次點擊執行**。管線會讀取現有 manifest，比對內文雜湊，**自動跳過所有已完成的 chunk**，僅從中斷點繼續合成。

---

## 五、完成後回到本地的發布流程

當 Colab 的 Step 10 完成後，所有成品都在 Google Drive 的 `audiobook-workspace/output/`：

1. **下載音檔**：
   將 `output/` 內的 13 個 `.wav` 下載回本機：  
   `/Users/howard/Downloads/幽靈的禮物/volume-price-analysis-en-chapters/zh-simplified-tts/audio/`

2. **有聲書轉檔 (Apple Books M4A)**：
   參考 [`docs/apple-audiobook-conversion.md`](apple-audiobook-conversion.md) 使用 `ffmpeg` 轉成包含中繼資料的 AAC `.m4a` 並匯入「音樂」App。

3. **私人 Podcast 串流發布 (Cloudflare R2)**：
   在本機執行既有的發布腳本：
   ```bash
   python "/Users/howard/Downloads/幽靈的禮物/volume-price-analysis-en-chapters/zh-simplified-tts/publish_podcast.py"
   ```
   腳本會自動將章節上傳到 Cloudflare R2 `howard-audiobooks`，並更新線上 RSS feed (`feed.xml`)。
