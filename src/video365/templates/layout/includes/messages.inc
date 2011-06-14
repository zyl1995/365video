{% if messages %}
	{% for message in messages %}
		{% if message.tags %}
			<div class="{{ message.tags }}">{{ message }}</div>
		{% endif %}	
	{% endfor %}
{% endif %}

{% if form.errors and form.non_field_errors %}
			<div class="warning">{{ form.non_field_errors }}</div>
{% endif %}

