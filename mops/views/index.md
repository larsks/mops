# Test

- moves userid: {{profile.userId}}
- earliest data: {{profile.profile.firstDate}}

<ul>
{% for entry in summary %}
<li><p>{{entry.date}}</p>
<ul>
<li><a href="/api/day/{{entry.date}}.gpx">as gpx</a> |
<a href="/api/day/{{entry.date}}.json">as json</a>
</li>
{% if entry.summary %}
{% for activity in entry.summary %}
<li>{{ activity.activity }} for {{activity.distance}} meters</li>
{% endfor %}
{% endif %}
</ul>
{% endfor %}
</ul>

