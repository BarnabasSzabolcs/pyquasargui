*********
Changelog
*********

Planned features:
=================
- Dialog, Banner
- Badge, FloatingActionButton
- Img, Video
- LinearProgress, CircularProgress, AjaxBar (could be as Progress + options...)
- MarkupTable (if pagination is needed then Table...)
- Rating
- ScrollArea
- Stepper (Wizard)
- Tabs, TabPanels


0.1
=====

- Initial release
- builds gui of any combination of quasar components
- supports matplotlib plots via Plot 
  (both non-interactive aka displaying png and interactive via mpld3)
- Enables dynamic children
- v-if, v-for, stc. as props, with Computed or Model as dynamically updated value
- deep Model's
- ability to add external scripts and styles
- known issues:
  - 'change' event does not fire (workaround: use Model.add_callback)
  - Editor is not editable (no workaround)

