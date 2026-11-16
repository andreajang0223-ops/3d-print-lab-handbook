// 3D 列印實驗室手冊｜首頁列表與搜尋
// 頁面清單只來自 data/pages.json（見 CLAUDE.md 第 6、7 節），不要在 index.html 手寫列表。

const SECTIONS = [
  { key: "materials", label: "線材", note: "材料特性與建議設定" },
  { key: "printers", label: "印表機", note: "機台規格與操作注意事項" },
  { key: "troubleshooting", label: "問題排解", note: "失敗症狀 → 原因 → 排除步驟" },
  { key: "logs", label: "實測紀錄", note: "實驗室實際列印驗證過的數據" },
];
const BADGE = { "參考值": "ref", "實測": "tested", "待確認": "todo" };

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function card(p) {
  const tags = (p.tags || []).map((t) => `<span class="tag">${esc(t)}</span>`).join("");
  return `<a class="card" href="${esc(p.path)}" data-search="${esc([p.title, p.summary, ...(p.tags || [])].join(" ").toLowerCase())}">
    <div class="title"><span>${esc(p.title)}</span><span class="badge ${BADGE[p.status] || "ref"}">${esc(p.status)}</span></div>
    <div class="summary">${esc(p.summary)}</div>
    <div class="tags">${tags}</div>
  </a>`;
}

async function renderIndex() {
  const root = document.getElementById("sections");
  if (!root) return;
  let pages = [];
  try {
    const res = await fetch("data/pages.json", { cache: "no-store" });
    pages = await res.json();
  } catch (e) {
    root.innerHTML = '<p class="empty">無法讀取 data/pages.json。請透過網站網址（GitHub Pages）或本機伺服器開啟。</p>';
    return;
  }
  root.innerHTML = SECTIONS.map((s) => {
    const list = pages.filter((p) => p.section === s.key).sort((a, b) => a.title.localeCompare(b.title, "zh-Hant"));
    return `<section class="section-block" id="${s.key}">
      <h2>${s.label}<span class="count">${list.length} 頁｜${s.note}</span></h2>
      <div class="cards">${list.map(card).join("") || '<p class="empty">尚無頁面。</p>'}</div>
    </section>`;
  }).join("");

  const latest = [...pages].sort((a, b) => b.updated.localeCompare(a.updated))[0];
  const stamp = document.getElementById("latest");
  if (stamp && latest) stamp.textContent = `共 ${pages.length} 頁，最近更新：${latest.updated}（${latest.title}）`;

  const box = document.getElementById("search");
  if (box) {
    box.addEventListener("input", () => {
      const q = box.value.trim().toLowerCase();
      document.querySelectorAll(".card").forEach((c) => {
        c.style.display = !q || c.dataset.search.includes(q) ? "" : "none";
      });
    });
  }
}

renderIndex();
