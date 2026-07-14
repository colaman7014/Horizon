---
layout: home
title: 每日新聞彙整
---

# 每日新聞彙整

<p><a href="{{ '/github-trending/' | relative_url }}">📈 GitHub 每日趨勢 Top 10 →</a></p>

<section class="daily-index" aria-labelledby="daily-complete-heading">
  <h2 id="daily-complete-heading">已完成彙整</h2>
  <ul>
    {% assign zh_posts = site.posts | where: "lang", "zh" %}
    {% for post in zh_posts limit:20 %}
      <li>
        <a href="{{ post.url | relative_url }}">{{ post.date | date: "%Y-%m-%d" }}</a>
      </li>
    {% else %}
      <li><em>尚無每日彙整</em></li>
    {% endfor %}
  </ul>
</section>
