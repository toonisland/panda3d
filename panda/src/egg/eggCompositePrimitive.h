// Filename: eggCompositePrimitive.h
// Created by:  drose (13Mar05)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) 2001 - 2004, Disney Enterprises, Inc.  All rights reserved
//
// All use of this software is subject to the terms of the Panda 3d
// Software license.  You should have received a copy of this license
// along with this source code; you will also find a current copy of
// the license at http://etc.cmu.edu/panda3d/docs/license/ .
//
// To contact the maintainers of this program write to
// panda3d-general@lists.sourceforge.net .
//
////////////////////////////////////////////////////////////////////

#ifndef EGGCOMPOSITEPRIMITIVE_H
#define EGGCOMPOSITEPRIMITIVE_H

#include "pandabase.h"

#include "eggPrimitive.h"

////////////////////////////////////////////////////////////////////
//       Class : EggCompositePrimitive
// Description : The base class for primitives such as triangle strips
//               and triangle fans, which include several component
//               triangles, each of which might have its own color
//               and/or normal.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDAEGG EggCompositePrimitive : public EggPrimitive {
PUBLISHED:
  INLINE EggCompositePrimitive(const string &name = "");
  INLINE EggCompositePrimitive(const EggCompositePrimitive &copy);
  INLINE EggCompositePrimitive &operator = (const EggCompositePrimitive &copy);
  INLINE ~EggCompositePrimitive();

  INLINE int get_num_components() const;
  INLINE const EggAttributes *get_component(int i) const;
  INLINE EggAttributes *get_component(int i);
  INLINE void set_component(int i, const EggAttributes *attrib);

  INLINE bool triangulate_into(EggGroupNode *container) const;
  PT(EggCompositePrimitive) triangulate_in_place();

  virtual void unify_attributes();
  virtual void apply_last_attribute();
  virtual void post_apply_last_attribute();
  virtual bool cleanup();

protected:
  virtual void prepare_add_vertex(EggVertex *vertex, int i, int n);
  virtual void prepare_remove_vertex(EggVertex *vertex, int i, int n);

  virtual bool do_triangulate(EggGroupNode *container) const=0;

  void write_body(ostream &out, int indent_level) const;

private:
  typedef pvector<EggAttributes *> Components;
  Components _components;

public:

  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    EggPrimitive::init_type();
    register_type(_type_handle, "EggCompositePrimitive",
                  EggPrimitive::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;

};

#include "eggCompositePrimitive.I"

#endif
