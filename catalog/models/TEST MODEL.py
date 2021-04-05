class Category(MPTTModel, TranslatableModel):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    translations = TranslatedFields(
        _title=models.CharField(blank=False, default='', db_index=True, max_length=128),
        _slug=models.SlugField(blank=False, default='', db_index=True, unique=True, max_length=128)
    )
    title = models.CharField(max_length=128)
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False,max_length=128, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        #ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.safe_translation_getter('title', any_language=True))
        super(Category, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})