require('./../utils/jquery-slidefade');

var $ = require('jquery');
var t = require('../utils/translate');

require('jquery-ui/ui/core');
require('jquery-ui/ui/widget');
require('jquery-ui/ui/mouse');
require('jquery-ui/ui/draggable');
require('jquery-ui/ui/droppable');
require('jquery-ui/ui/sortable');
require('jquery-ui/ui/resizable');
require('jquery-ui/ui/button');
require('jquery-ui/ui/dialog');

var Dashboard = function($dashboard) {
    this.$dashboard = $dashboard;
};

Dashboard.prototype = {
    initTools: function($dashboard) {
        $dashboard.find('.dashboard-bases-tools-toggle').on('click', function (e) {
            e.preventDefault();
            $dashboard.find('.dashboard-bases-tools').toggleClass('visible');
        });

        var $form = $dashboard.find('#add-dashboard-bases-module-form');

        $form.find('.add-dashboard-bases-link').on('click', function (e) {
            var $typeInput = $form.find('[name="type"]');
            var type = $form.find('[name="module"] option:selected').data('type');

            if (type) {
                $typeInput.val(type);

                $.ajax({
                    url: $form.attr('action'),
                    method: $form.attr('method'),
                    dataType: 'json',
                    data: $form.serialize(),
                    success: function (result) {
                        if (result.error) {
                            return;
                        }

                        document.location = result.success_url;
                    }
                });
            }

            e.preventDefault();
        });

        $dashboard.find('.reset-dashboard-bases-link').on('click', function(e) {
            var buttons = {};
            var resetDashboard = function () {
                var $form = $dashboard.find('#reset-dashboard-bases-form');

                $.ajax({
                    url: $form.attr('action'),
                    method: $form.attr('method'),
                    dataType: 'json',
                    data: $form.serialize(),
                    success: function (result) {
                        if (result.error) {
                            return;
                        }

                        location.reload();
                    }
                });
            };

            buttons[t('Yes')] = function() {
                resetDashboard();
                $(this).dialog('close');
            };

            buttons[t('Cancel')] = function() {
                $(this).dialog('close');
            };

            $dashboard.find('#reset-dashboard-bases-dialog').dialog({
                resizable: false,
                modal: true,
                buttons: buttons
            });

            e.preventDefault();
        });
    },
    updateDashboardModules: function($dashboard) {
        var $form = $dashboard.find('#update-dashboard-bases-modules-form');
        var modules = [];

        $dashboard.find('.dashboard-bases-column').each(function () {
            var $column = $(this);
            var column = $column.closest('.dashboard-bases-column-wrapper').index();

            $column.find('.dashboard-bases-item').each(function () {
                var $item = $(this);
                var order = $item.index();
                var id = $item.data('module-id');

                modules.push({
                    id: id,
                    column: column,
                    order: order
                });
            });
        });

        $form.find('[name="modules"]').val(JSON.stringify(modules));

        $.ajax({
            url: $form.attr('action'),
            method: $form.attr('method'),
            dataType: 'json',
            data: $form.serialize()
        });
    },
    initModulesDragAndDrop: function($dashboard) {
        var self = this;

        $dashboard.find('.dashboard-bases-column').droppable({
            activeClass: 'active',
            hoverClass: 'hovered',
            tolerance: 'pointer',
            accept: '.dashboard-bases-item'
        }).sortable({
            items: '.dashboard-bases-item.draggable',
            handle: '.dashboard-bases-item-header',
            tolerance: 'pointer',
            connectWith: '.dashboard-bases-column',
            cursor: 'move',
            placeholder: 'dashboard-bases-item placeholder',
            forcePlaceholderSize: true,
            update: function (event, ui) {
                self.updateDashboardModules($dashboard);
            }
        });
    },
    initCollapsibleModules: function($dashboard) {
        var $form = $dashboard.find('#update-dashboard-bases-module-collapse-form');

        $dashboard.find('.dashboard-bases-item.collapsible').each(function () {
            var $item = $(this);
            var $link = $item.find('.dashboard-bases-item-collapse');
            var $collapsible = $item.find('.dashboard-bases-item-content');
            var moduleId = $item.data('module-id');

            $link.on('click', function (e) {
                e.preventDefault();

                $collapsible.slideFadeToggle(200, 'swing', function () {
                    var collapsed = $collapsible.is(':visible') == false;

                    if (collapsed) {
                        $item.addClass('collapsed')
                    } else {
                        $item.removeClass('collapsed')
                    }

                    $form.find('[name="id"]').val(moduleId);
                    $form.find('[name="collapsed"]').val(collapsed ? 'true' : 'false');

                    $.ajax({
                        url: $form.attr('action'),
                        method: $form.attr('method'),
                        dataType: 'json',
                        data: $form.serialize()
                    });
                });
            });
        });
    },
    initDeletableModules: function($dashboard) {
        var $form = $dashboard.find('#remove-dashboard-bases-module-form');

        $dashboard.find('.dashboard-bases-item.deletable').each(function () {
            var $item = $(this);
            var $link = $item.find('.dashboard-bases-item-remove');
            var moduleId = $item.data('module-id');

            $link.on('click', function (e) {
                e.preventDefault();

                var buttons = {};

                var deleteModule = function () {
                    $item.fadeOut(200, 'swing', function () {
                        $form.find('[name="id"]').val(moduleId);

                        $.ajax({
                            url: $form.attr('action'),
                            method: $form.attr('method'),
                            dataType: 'json',
                            data: $form.serialize()
                        });
                    });
                };

                buttons[t('Delete')] = function () {
                    deleteModule();
                    $(this).dialog('close');
                };

                buttons[t('Cancel')] = function () {
                    $(this).dialog('close');
                };

                $dashboard.find('#module-remove-dialog').dialog({
                    resizable: false,
                    modal: true,
                    buttons: buttons
                });
            });
        });
    },
    initAjaxModules: function($dashboard) {
        $dashboard.find('.dashboard-bases-item.ajax').each(function () {
            var $item = $(this);
            var $content = $item.find('.dashboard-bases-item-content');
            var url = $item.data('ajax-url');

            $.ajax({
                url: url,
                dataType: 'json',
                success: function (result) {
                    if (result.error) {
                        $content.empty();
                        return;
                    }

                    var oldHeight = $content.height();
                    $content.html(result.html);
                    var newHeight = $content.height();

                    $content.height(oldHeight);
                    $content.animate({
                        height: newHeight
                    }, 250, 'swing', function() {
                        $content.height('auto');
                    });
                },
                error: function () {
                    $content.empty();
                }
            });
        });
    },
    updateModuleChildrenFormsetLabels: function($inline) {
        $inline.find('.inline-related').each(function(i) {
            $(this).find('.inline_label').text('#' + (i + 1));
        });
    },
    updateModuleChildrenFormsetFormIndex: function($form, index) {
        var prefix = "children";
        var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
        var replacement = prefix + "-" + index;

        $form.find("fieldset.module *").each(function() {
            var $el = $(this);

            $.each(['for', 'id', 'name'], function() {
                var attr = this;

                if ($el.attr(attr)) {
                    $el.attr(attr, $el.attr(attr).replace(id_regex, replacement));
                }
            });
        });
    },
    updateModuleChildrenFormsetFormsIndexes: function($inline) {
        var self = this;
        var from = parseInt($inline.find('.inline-related.has_original').length);

        $inline.find('.inline-related.last-related').each(function(i) {
            self.updateModuleChildrenFormsetFormIndex($(this), from + i);
        });
    },
    updateModuleChildrenFormsetTotalForms: function($inline) {
        var $totalFormsInput = $inline.find('[name="children-TOTAL_FORMS"]');
        var totalForms = parseInt($inline.find('.inline-related').length);

        $totalFormsInput.val(totalForms);
    },
    initModuleChildrenFormsetUpdate: function($dashboard) {
        if (!$dashboard.hasClass('change-form')) {
            return;
        }

        var self = this;
        var $inline = $dashboard.find('.inline-group');

        $inline.find('.add-row a').on('click', function(e) {
            e.preventDefault();

            var $empty = $inline.find('.inline-related.empty-form');
            var $clone = $empty
                .clone(true)
                .removeClass('empty-form')
                .insertBefore($empty);

            self.updateModuleChildrenFormsetLabels($inline);
            self.updateModuleChildrenFormsetFormIndex($empty, parseInt($inline.find('.inline-related').length) - 1);
            self.updateModuleChildrenFormsetFormIndex($clone, parseInt($inline.find('.inline-related').length) - 2);
            self.updateModuleChildrenFormsetTotalForms($inline);
        });

        $inline.find('.inline-deletelink').on('click', function(e) {
            e.preventDefault();

            $(this).closest('.inline-related').remove();

            self.updateModuleChildrenFormsetFormsIndexes($inline);
            self.updateModuleChildrenFormsetLabels($inline);
            self.updateModuleChildrenFormsetTotalForms($inline);
        });
    },
    run: function() {
        var $dashboard = this.$dashboard;

        try {
            this.initTools($dashboard);
            this.initModulesDragAndDrop($dashboard);
            this.initCollapsibleModules($dashboard);
            this.initDeletableModules($dashboard);
            this.initAjaxModules($dashboard);
            this.initModuleChildrenFormsetUpdate($dashboard);
        } catch (e) {
            console.error(e, e.stack);
        }

        $dashboard.addClass('initialized');
    }
};

$(document).ready(function() {
    $('.dashboard-bases.jet').each(function() {
        new Dashboard($(this)).run();
    });
});
