{% load i18n %}
{% if videoposts.object_list %}
{% for videopost in videoposts.object_list %}
{% include "videopost/includes/videopost.inc" %}
{% endfor%}
{% include "videopost/includes/player_js.inc" %}
{% if videoposts.has_previous or videoposts.has_next %}
<table class="pagination">
    <td class="pagination-left">
        {% if videoposts.has_previous %}<a class="pagination-left" href="{{ PATH }}{{ videoposts.previous_page_number }}/">{% trans 'Previous' %}</a>
        {% endif %} 
    </td>
    <td class="pagination-center">
        <span class="pagination-center">{% trans 'Page' %} {{ videoposts.number }} {% trans 'of' %} {{ videoposts.paginator.num_pages }}.</span>
    </td>
    <td class="pagination-right" >
        {% if videoposts.has_next %}<a class="pagination-right" href="{{ PATH }}{{ videoposts.next_page_number }}/">{% trans 'Next' %}</a>
        {% endif %} 
    </td>
</table>
{% endif %}
{% endif %}
