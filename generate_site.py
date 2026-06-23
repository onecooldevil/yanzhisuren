#!/usr/bin/env python3
"""
generate_site.py
从 anchor_data_new.json 生成嵌入全量数据的 public-site/index.html
每次数据更新后运行此脚本即可刷新页面。
用法：python3 generate_site.py
"""

import json, os, re, sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, '..', 'data', 'anchor_data_latest.json')
# 也支持直接传参指定数据文件
if len(sys.argv) > 1:
    DATA_FILE = sys.argv[1]

DATA_FILE = os.path.abspath(DATA_FILE)
OUT_FILE  = os.path.join(BASE, 'index.html')

print(f'读取数据: {DATA_FILE}')
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    raw = json.load(f)

records = []
for r in raw:
    # 兼容两种格式：青雀读取的原始中文键 或 已转换的英文键
    def g(*keys):
        for k in keys:
            v = r.get(k)
            if v is not None and str(v).strip() not in ('', 'None'):
                return re.sub(r'\.0$', '', str(v).strip())
        return ''

    ks = g('快手ID', 'ks_id')
    if ks in ('0', '0.0'):
        ks = ''

    records.append([
        g('主播ID', 'anchor_id'),
        ks,
        g('主播昵称', 'anchor_name'),
        g('奖励明细\n小火苗/涨粉/流量券', '奖励明细', 'reward'),
        g('奖励原因\n返点活动报名/入群备注奖励等', '奖励原因', 'reason'),
        g('奖励填入时间', '奖励登记时间', 'fill_time'),
        g('预计生效时间', 'eff_time'),
        g('是否配置&配置人', '是否配置', 'status'),
    ])

data_js = json.dumps(records, ensure_ascii=False, separators=(',', ':'))
now_str = datetime.now().strftime('%Y-%m-%d %H:%M')

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>颜值素人主播 · 获奖明细查询</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
  :root {{
    --orange: #FF5002;
    --orange-light: #FF7234;
    --cream: #FFF8F4;
    --gray: #F5F0EC;
    --text: #2D1500;
    --text-light: #8A6A55;
    --border: #F0E4D8;
    --green: #00B96B;
    --shadow: 0 4px 24px rgba(255,80,2,0.12);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Noto Sans SC', 'PingFang SC', 'Helvetica Neue', sans-serif; background: var(--cream); color: var(--text); min-height: 100vh; -webkit-font-smoothing: antialiased; }}
  .hero {{ background: linear-gradient(135deg, #FF4500 0%, #FF5002 40%, #FF7234 100%); padding: 44px 20px 54px; text-align: center; position: relative; overflow: hidden; }}
  .hero::before {{ content: ''; position: absolute; top: -50px; right: -50px; width: 220px; height: 220px; border-radius: 50%; background: rgba(255,255,255,0.08); }}
  .hero::after {{ content: ''; position: absolute; bottom: -70px; left: -30px; width: 180px; height: 180px; border-radius: 50%; background: rgba(255,255,255,0.05); }}
  .hero-badge {{ display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.35); border-radius: 20px; padding: 5px 14px; font-size: 12px; font-weight: 500; color: #fff; margin-bottom: 14px; backdrop-filter: blur(4px); position: relative; z-index: 1; }}
  .hero h1 {{ font-size: 28px; font-weight: 900; color: #fff; line-height: 1.2; margin-bottom: 8px; letter-spacing: -0.5px; position: relative; z-index: 1; }}
  .hero p {{ font-size: 13px; color: rgba(255,255,255,0.85); position: relative; z-index: 1; }}
  .hero-wave {{ position: absolute; bottom: 0; left: 0; right: 0; height: 22px; background: var(--cream); border-radius: 22px 22px 0 0; }}
  .search-wrap {{ margin: -20px 16px 0; position: relative; z-index: 10; }}
  .search-box {{ background: #fff; border-radius: 18px; padding: 20px; box-shadow: var(--shadow); border: 1px solid var(--border); }}
  .search-label {{ font-size: 13px; font-weight: 600; color: var(--text-light); margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
  .search-label::before {{ content: '🔍'; }}
  .input-row {{ display: flex; flex-direction: column; gap: 10px; }}
  .input-field {{ width: 100%; border: 1.5px solid var(--border); border-radius: 12px; padding: 14px 16px; font-size: 16px; color: var(--text); outline: none; background: var(--gray); font-family: inherit; transition: border-color 0.2s, background 0.2s; }}
  .input-field:focus {{ border-color: var(--orange); background: #fff; box-shadow: 0 0 0 3px rgba(255,80,2,0.08); }}
  .btn-search {{ width: 100%; background: linear-gradient(135deg, var(--orange), var(--orange-light)); color: #fff; border: none; border-radius: 12px; padding: 15px 20px; font-size: 17px; font-weight: 700; cursor: pointer; font-family: inherit; box-shadow: 0 4px 14px rgba(255,80,2,0.28); transition: transform 0.15s; letter-spacing: 2px; }}
  .btn-search:active {{ transform: scale(0.98); }}
  .input-hint {{ font-size: 11px; color: var(--text-light); margin-top: 4px; padding: 0 2px; }}
  .content {{ padding: 16px 16px 100px; }}
  .initial-state {{ text-align: center; padding: 52px 24px; }}
  .initial-icon {{ font-size: 52px; margin-bottom: 16px; display: block; }}
  .initial-state h3 {{ font-size: 17px; font-weight: 700; color: var(--text); margin-bottom: 8px; }}
  .initial-state p {{ font-size: 13px; color: var(--text-light); line-height: 1.7; }}
  .result-profile {{ background: #fff; border-radius: 14px; padding: 16px; margin-bottom: 14px; border: 1px solid var(--border); display: flex; align-items: center; gap: 14px; animation: popIn 0.35s cubic-bezier(0.34,1.56,0.64,1); }}
  .avatar {{ width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, var(--orange), var(--orange-light)); display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; }}
  .profile-info {{ flex: 1; }}
  .profile-name {{ font-size: 18px; font-weight: 800; color: var(--text); margin-bottom: 4px; }}
  .profile-sub {{ font-size: 12px; color: var(--text-light); }}
  .reward-badge {{ background: linear-gradient(135deg, var(--orange), var(--orange-light)); color: #fff; border-radius: 20px; padding: 5px 12px; font-size: 12px; font-weight: 700; white-space: nowrap; flex-shrink: 0; }}
  .reward-card {{ background: #fff; border-radius: 14px; margin-bottom: 12px; border: 1px solid var(--border); overflow: hidden; animation: fadeUp 0.35s cubic-bezier(0.34,1.56,0.64,1) both; }}
  .reward-card:nth-child(1) {{ animation-delay: 0.05s; }} .reward-card:nth-child(2) {{ animation-delay: 0.1s; }} .reward-card:nth-child(3) {{ animation-delay: 0.15s; }} .reward-card:nth-child(n+4) {{ animation-delay: 0.2s; }}
  .reward-head {{ background: linear-gradient(135deg, #FFF2EB, #FFE8D6); padding: 13px 16px 10px; border-bottom: 1px solid #FFE0CC; display: flex; align-items: center; gap: 10px; }}
  .reward-num {{ width: 22px; height: 22px; border-radius: 50%; background: var(--orange); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 800; flex-shrink: 0; }}
  .reward-title-text {{ font-size: 15px; font-weight: 800; color: var(--orange); flex: 1; }}
  .reward-body {{ padding: 14px 16px; }}
  .detail-row {{ display: flex; align-items: flex-start; gap: 10px; padding: 7px 0; border-bottom: 1px solid var(--gray); }}
  .detail-row:last-child {{ border-bottom: none; padding-bottom: 0; }}
  .dl {{ font-size: 12px; color: var(--text-light); font-weight: 500; min-width: 66px; flex-shrink: 0; padding-top: 1px; }}
  .dv {{ font-size: 13px; color: var(--text); font-weight: 600; flex: 1; line-height: 1.5; }}
  .status-ok {{ display: inline-flex; align-items: center; gap: 3px; background: #E8F8F0; color: var(--green); border-radius: 6px; padding: 2px 8px; font-size: 12px; font-weight: 600; }}
  .status-ok::before {{ content: '✓'; font-weight: 800; }}
  .status-pending {{ display: inline-flex; align-items: center; gap: 3px; background: #FFF3E0; color: #E67E00; border-radius: 6px; padding: 2px 8px; font-size: 12px; font-weight: 600; }}
  .not-found {{ text-align: center; padding: 48px 24px; animation: popIn 0.35s cubic-bezier(0.34,1.56,0.64,1); }}
  .not-found-icon {{ font-size: 48px; margin-bottom: 14px; display: block; }}
  .not-found h3 {{ font-size: 17px; font-weight: 700; color: var(--text); margin-bottom: 8px; }}
  .not-found p {{ font-size: 13px; color: var(--text-light); line-height: 1.7; }}
  .section-label {{ font-size: 12px; color: var(--text-light); font-weight: 600; padding: 0 4px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
  .section-label::before {{ content: ''; display: block; width: 3px; height: 12px; background: var(--orange); border-radius: 2px; }}
  .footer {{ position: fixed; bottom: 0; left: 0; right: 0; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-top: 1px solid var(--border); padding: 10px 16px calc(10px + env(safe-area-inset-bottom)); text-align: center; }}
  .footer p {{ font-size: 11px; color: var(--text-light); }}
  @keyframes popIn {{ from {{ opacity: 0; transform: scale(0.92); }} 60% {{ transform: scale(1.02); }} to {{ opacity: 1; transform: scale(1); }} }}
  @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: translateY(0); }} }}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-badge">🎖️ 颜值品类 · 素人主播专属</div>
  <h1>获奖明细查询</h1>
  <p>输入主播ID或快手号，即可查询您的专属奖励</p>
  <div class="hero-wave"></div>
</div>

<div class="search-wrap">
  <div class="search-box">
    <div class="search-label">查询我的奖励</div>
    <div class="input-row">
      <input type="text" class="input-field" id="search-input"
        placeholder="请输入您的主播ID或快手号"
        autocomplete="off" autocorrect="off" autocapitalize="off" inputmode="text"
        onkeydown="if(event.key==='Enter')doSearch()">
      <button class="btn-search" onclick="doSearch()">查询我的奖励</button>
    </div>
    <div class="input-hint">支持主播数字ID（如 123456789）或快手号（如 kuaishouuser01）</div>
  </div>
</div>

<div class="content" id="content">
  <div class="initial-state">
    <span class="initial-icon">🏆</span>
    <h3>查询您的专属奖励</h3>
    <p>在上方输入您的主播ID或快手号<br>即可查看您的全部获奖明细</p>
  </div>
</div>

<div class="footer">
  <p>颜值品类运营团队 · 数据仅供参考，以实际发放为准 · 更新于 {now_str}</p>
</div>

<script>
// DATA格式: [anchor_id, ks_id, name, reward, reason, fill_time, eff_time, status]
var RAW={data_js};
var idxById={{}},idxByKs={{}};
RAW.forEach(function(r){{
  if(r[0]){{if(!idxById[r[0]])idxById[r[0]]=[];idxById[r[0]].push(r);}}
  if(r[1]){{if(!idxByKs[r[1]])idxByKs[r[1]]=[];idxByKs[r[1]].push(r);}}
}});
function fmtDate(d){{if(!d||d==='')return'-';var s=String(d).trim();if(/^\\d{{8}}$/.test(s))return s.slice(0,4)+'年'+s.slice(4,6)+'月'+s.slice(6,8)+'日';return s;}}
function esc(s){{return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}}
function statusHtml(s){{if(!s||s==='')return'<span class="status-pending">配置中…</span>';if(s.indexOf('已配置')!==-1)return'<span class="status-ok">已配置</span>';return'<span class="status-pending">配置中…</span>';}}
function setLoading(on){{var b=document.querySelector('.btn-search');if(!b)return;b.disabled=on;b.style.opacity=on?'0.7':'1';b.textContent=on?'查询中...':'查询我的奖励';}}
function renderNotFound(){{document.getElementById('content').innerHTML='<div class="not-found"><span class="not-found-icon">🔎</span><h3>未找到获奖记录</h3><p>未查到该主播ID或快手号的获奖信息<br>请确认输入是否正确，或联系运营人员咨询</p></div>';}}
function toRow(r){{return{{id:r[0],ks:r[1],name:r[2],reward:r[3],reason:r[4],fill:r[5],eff:r[6],status:r[7]}};}}
function dedupe(rows){{var seen={{}};return rows.filter(function(r){{var k=[r.id,r.reward,r.fill].join('||');if(seen[k])return false;seen[k]=true;return true;}});}}
function renderRows(sorted){{
  var a=sorted[0],html='';
  html+='<div class="result-profile"><div class="avatar">🎤</div><div class="profile-info"><div class="profile-name">'+esc(a.name)+'</div><div class="profile-sub">ID: '+esc(a.id||'-')+'</div>'+(a.ks?'<div class="profile-sub">快手号: '+esc(a.ks)+'</div>':'')+'</div><div class="reward-badge">共'+sorted.length+'项奖励</div></div>';
  html+='<div class="section-label">获奖明细（最新在前）</div>';
  sorted.forEach(function(r,i){{
    html+='<div class="reward-card"><div class="reward-head"><div class="reward-num">'+(i+1)+'</div><div class="reward-title-text">'+esc(r.reward)+'</div></div><div class="reward-body">';
    html+='<div class="detail-row"><span class="dl">获奖原因</span><span class="dv">'+esc(r.reason||'-')+'</span></div>';
    html+='<div class="detail-row"><span class="dl">获奖时间</span><span class="dv">'+esc(fmtDate(r.fill))+'</span></div>';
    html+='<div class="detail-row"><span class="dl">预计生效</span><span class="dv">'+esc(fmtDate(r.eff))+'</span></div>';
    html+='<div class="detail-row"><span class="dl">是否配置</span>'+statusHtml(r.status)+'</div>';
    html+='</div></div>';
  }});
  var c=document.getElementById('content');c.innerHTML=html;c.scrollIntoView({{behavior:'smooth',block:'start'}});
}}
function doSearch(){{
  var val=document.getElementById('search-input').value.trim();
  if(!val){{document.getElementById('search-input').focus();return;}}
  setLoading(true);
  setTimeout(function(){{
    try{{
      var hits=[];
      (idxById[val]||[]).concat(/[^0-9]/.test(val)?(idxByKs[val]||[]):[]).forEach(function(r){{hits.push(toRow(r));}});
      hits=dedupe(hits);
      if(!hits.length){{renderNotFound();return;}}
      renderRows(hits.slice().sort(function(a,b){{var fa=String(a.fill||''),fb=String(b.fill||'');return fb>fa?1:fb<fa?-1:0;}}));
    }}finally{{setLoading(false);}}
  }},30);
}}
</script>
</body>
</html>"""

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(OUT_FILE) / 1024
print(f'✅ 生成完成: {OUT_FILE}')
print(f'   条数: {len(records)}  文件大小: {size_kb:.1f} KB  更新时间: {now_str}')
