class PostStatus:
    DRAFT = "draft"
    PROCESSING = "processing"
    PUBLISHED = "published"

    CHOICES = [
        (DRAFT, "Draft"),
        (PROCESSING, "Processing"),
        (PUBLISHED, "Published"),
    ]


class PostVisibility:
    HIDDEN = "hidden"
    VISIBLE = "visible"

    CHOICES = [
        (HIDDEN, "Hidden"),
        (VISIBLE, "Visible"),
    ]
