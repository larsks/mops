# Test

- moves userid: {{profile.userId}}
- earliest data: {{profile.profile.firstDate}}

<ul>
{% for entry in summary %}
<li><p>{{entry.date}}</p>
<ul>
{% for activity in entry.summary %}
<li>{{ activity.activity }} for {{activity.distance}} meters</li>
{% endfor %}
</ul>
{% endfor %}
</ul>

