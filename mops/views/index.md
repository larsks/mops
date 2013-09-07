# Test

- moves userid: {{profile.userId}}
- earliest data: {{profile.profile.firstDate}}
- token: {{session.moves_access_token}}

<ul>
{% for entry in summary %}
<li><p>{{entry.date}}</p>
<ul>
<li><a href="/api/day/{{entry.date}}.gpx">as gpx</a> |
<a href="/api/day/{{entry.date}}.json">as json</a>
</li>
{% for activity in entry.summary %}
<li>{{ activity.activity }} for {{activity.distance}} meters</li>
{% endfor %}
</ul>
{% endfor %}
</ul>

