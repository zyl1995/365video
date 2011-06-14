{% load i18n %}
{% load humanize %}
<div class="videopost">
    <a href="{{ videopost.get_absolute_url }}"><h1 class="videopost-title">{{ videopost.title }}</h1></a>
    <h3 class="videopost-date-header">{{ videopost.publication_date|naturalday}}</h3>
    <div class="videopost-video">
		<a class="player" href="{{ MEDIA_URL }}{{ videopost.video }}" style="background-image:url('{{ MEDIA_URL }}{{ videopost.splash_image }}');" id="player">&nbsp;</a>
    </div>
    <p class="videopost-description">
    {{ videopost.description }}
    </p>
    {% if videopost.tags.all %}
    <p class="videopost-labels">
        Labels:&nbsp; 
        {% for tag in videopost.tags.all %} 
	        {% if forloop.first %}  
	        <a href="{{ tag.get_absolute_url }}">{{ tag }}</a>{% else %}, <a href="{{ tag.get_absolute_url }}">{{ tag }}</a> 
	        {% endif %} 
        {% endfor %}
    </p>
    {% endif %}
</div>