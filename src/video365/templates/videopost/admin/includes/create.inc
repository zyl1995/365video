        <tr>
            <td>
                {{ form.title.label_tag }}:
            </td>
            <td>
                {{ form.title }}
            </td>
        </tr>
        <tr>
            <td>

            </td>
            <td>
                {{ form.title.errors }}
            </td>
        </tr>
        <tr>
            <td>
               {{ form.video.label_tag }}:
            </td>
            <td>
                <input type="file" id="id_video" name="video" size="28px">
            </td>
        </tr>
        <tr>
            <td>

            </td>
            <td>
                {{ form.video.errors }}
            </td>
        </tr>
        <tr>
            <td>
                {{ form.splash_image.label_tag }}:
            </td>
            <td>
                <input type="file" id="id_splash_image" name="splash_image" size="28px">
            </td>
        </tr>
        <tr>
            <td>

            </td>
            <td>
                {{ form.splash_image.errors }}
            </td>
        </tr>
        <tr>
            <td>
                {{ form.enabled.label_tag }}:
            </td>
            <td>
                {{ form.enabled }}
            </td>
        </tr>
        <tr>
            <td>

            </td>
            <td>
                {{ form.enabled.errors }}
            </td>
        </tr>
        <tr>
            <td>
                {{ form.description.label_tag }}:
            </td>
            <td>
                {{ form.description }}
            </td>
        </tr>
        <tr>
            <td>

            </td>
            <td>
                {{ form.description.errors }}
            </td>
        </tr>
        <tr>
            <td>
                {{ form.tags.label_tag }}:
            </td>
            <td>
                {{ form.tags }}
            </td>
        </tr>
        <tr>
            <td>

            </td>
            <td>
                {{ form.tags.errors }}
            </td>
        </tr>
