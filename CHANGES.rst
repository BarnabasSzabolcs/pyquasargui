*********
Changelog
*********



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
  - QEditor is not editable (no workaround)

