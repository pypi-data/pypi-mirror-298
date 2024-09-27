#ifndef STST_PY_HPP
#define STST_PY_HPP

#include "structstore/stst_alloc.hpp"
#include "structstore/stst_containers.hpp"
#include "structstore/stst_field.hpp"
#include "structstore/stst_structstore.hpp"
#include "structstore/stst_typing.hpp"
#include "structstore/stst_utils.hpp"

#include <functional>
#include <iostream>
#include <stdexcept>
#include <unordered_map>

#include <nanobind/make_iterator.h>
#include <nanobind/nanobind.h>

// make customized STL containers opaque to nanobind
namespace nanobind::detail {
template<class T>
class type_caster<structstore::vector<T>>
    : public type_caster_base<structstore::vector<T>> {};

template<class K, class T>
class type_caster<structstore::unordered_map<K, T>>
    : public type_caster_base<structstore::unordered_map<K, T>> {};
} // namespace nanobind::detail

namespace structstore {

namespace nb = nanobind;

nb::object to_python(const StructStoreField& field, bool recursive);

void from_python(FieldAccess access, const nb::handle& value, const std::string& field_name);

class py {
private:
    static nb::object __slots__(StructStore& store);

    static nb::object get_field(StructStore& store, const std::string& name);

    static void set_field(StructStore& store, const std::string& name, const nb::object& value);

    static ScopedLock lock(StructStore& store);

    static nb::object __repr__(StructStore& store);

    static nb::object copy(StructStore& store);

    static nb::object deepcopy(StructStore& store);

    static nb::object __copy__(StructStore& store);

    static nb::object __deepcopy__(StructStore& store, nb::handle&);

    static void clear(StructStore& store);

public:
    static nb::object SimpleNamespace;

    using FromPythonFn = std::function<bool(FieldAccess, const nb::handle&)>;
    using ToPythonFn = std::function<nb::object(const StructStoreField&, bool recursive)>;

    static std::unordered_map<uint64_t, FromPythonFn>& get_from_python_fns();

    static std::unordered_map<uint64_t, ToPythonFn>& get_to_python_fns();

    template<typename T>
    static void register_from_python_fn(const FromPythonFn& from_python_fn) {
        uint64_t type_hash = typing::get_type_hash<T>();
        bool success = get_from_python_fns().insert({type_hash, from_python_fn}).second;
        if (!success) {
            throw typing::already_registered_type_error(type_hash);
        }
    }

    template<typename T>
    static void register_to_python_fn(const ToPythonFn& to_python_fn) {
        uint64_t type_hash = typing::get_type_hash<T>();
        bool success = get_to_python_fns().insert({type_hash, to_python_fn}).second;
        if (!success) {
            throw typing::already_registered_type_error(type_hash);
        }
    }

    template<typename T_cpp>
    static void register_basic_to_python() {
        register_to_python_fn<T_cpp>([](const StructStoreField& field, bool recursive) -> nb::object {
            return nb::cast(field.get<T_cpp>(), nb::rv_policy::reference);
        });
    }

    template<typename T_cpp, typename T_py>
    static void register_basic_py() {
        static_assert(!std::is_pointer<T_cpp>::value);
        register_to_python_fn<T_cpp>([](const StructStoreField& field, bool recursive) -> nb::object {
            return T_py(field.get<T_cpp>());
        });
        register_from_python_fn<T_cpp>([](FieldAccess access, const nb::handle& value) {
            if (nb::isinstance<T_py>(value)) {
                access.get<T_cpp>() = nb::cast<T_cpp>(value);
                return true;
            }
            return false;
        });
    }

    template<typename T>
    static void register_basic_py_funcs(nb::class_<T>& cls) {
        static_assert(!std::is_pointer<T>::value);
        cls.def("to_yaml", [=](T& t) {
            return YAML::Dump(to_yaml(*FieldView{t}));
        });
        cls.def("__repr__", [=](T& t) {
            return (std::ostringstream() << *FieldView{t}).str();
        });
        cls.def("copy", [=](T& t) {
            return structstore::to_python(*FieldView{t}, false);
        });
        cls.def("deepcopy", [=](T& t) {
            return structstore::to_python(*FieldView{t}, true);
        });
        cls.def("__copy__", [=](T& t) {
            return structstore::to_python(*FieldView{t}, false);
        });
        cls.def("__deepcopy__", [=](T& t, nb::handle&) {
            return structstore::to_python(*FieldView{t}, true);
        });
    }

    template<typename T>
    static void register_basic_py(nb::class_<T>& cls) {
        static_assert(!std::is_pointer<T>::value);
        register_to_python_fn<T>([](const StructStoreField& field, bool /*recursive*/) -> nb::object {
            return nb::cast(field.get<T>(), nb::rv_policy::reference);
        });
        register_from_python_fn<T>([cls](FieldAccess access, const nb::handle& value) {
            if (value.type().equal(cls)) {
                access.get<T>() = nb::cast<T&>(value);
                return true;
            }
            return false;
        });
        register_basic_py_funcs<T>(cls);
    }

    template<typename T_cpp>
    static void register_ptr_py(const nb::handle& T_ptr_py, const nb::handle& T_py) {
        static_assert(std::is_pointer<T_cpp>::value);
        register_basic_to_python<T_cpp>();
        register_from_python_fn<T_cpp>([T_ptr_py, T_py](FieldAccess access, const nb::handle& value) {
            if (value.type().equal(T_ptr_py) || (!access.get_field().empty() && value.type().equal(T_py))) {
                access.get<T_cpp>() = nb::cast<T_cpp>(value);
                return true;
            }
            return false;
        });
    }

    template<typename T_cpp>
    static bool object_from_python(FieldAccess access, const nb::handle& value) {
        try {
            T_cpp& value_cpp = nb::cast<T_cpp&>(value, false);
            T_cpp& field_cpp = access.get<T_cpp>();
            std::cout << "at type "
                      << typing::get_type_name(typing::get_type_hash<T_cpp>())
                      << std::endl;
            if (&value_cpp == &field_cpp) {
                std::cout << "copying to itself" << std::endl;
                return true;
            }
            std::cout << "copying " << typing::get_type_name(typing::get_type_hash<T_cpp>()) << " from " << &value_cpp << " to " << &field_cpp << std::endl;
            field_cpp = value_cpp;
            return true;
        } catch (const nb::cast_error&) {
        }
        return false;
    }

    template<typename T_cpp>
    static void register_object_from_python() {
        register_from_python_fn<T_cpp>(object_from_python<T_cpp>);
    }

    template<typename T>
    static void register_structstore_py(nb::class_<T>& cls) {
        register_basic_py_funcs<T>(cls);

        cls.def_prop_ro("__slots__", [](T& t) {
            auto& store = t.get_store();
            return __slots__(store);
        });

        cls.def("__getattr__", [](T& t, const std::string& name) {
            auto& store = t.get_store();
            return get_field(store, name); }, nb::arg("name"), nb::rv_policy::reference_internal);

        cls.def("__setattr__", [](T& t, const std::string& name, const nb::object& value) {
            auto& store = t.get_store();
            return set_field(store, name, value); }, nb::arg("name"), nb::arg("value").none());

        cls.def("__getitem__", [](T& t, const std::string& name) {
            auto& store = t.get_store();
            return get_field(store, name); }, nb::arg("name"), nb::rv_policy::reference_internal);

        cls.def("__setitem__", [](T& t, const std::string& name, const nb::object& value) {
            auto& store = t.get_store();
            return set_field(store, name, value); }, nb::arg("name"), nb::arg("value").none());

        cls.def("lock", [](T& t) {
            auto& store = t.get_store();
            return lock(store); }, nb::rv_policy::move);

        cls.def("clear", [](T& t) {
            auto& store = t.get_store();
            return clear(store);
        });

        cls.def("check", [](T& t) {
            std::cout << "checking from python ..." << std::endl;
            auto& store = t.get_store();
            return store.check();
        });
    }

protected:
    template<typename T>
    static void _from_python(T& t, MiniMalloc& mm_alloc,
                             const nb::handle& value,
                             const std::string& field_name) {
        structstore::from_python(*AccessView{t, mm_alloc}, value, field_name);
    }

    template<typename T>
    static nb::object _to_python(T& t, bool recursive) {
        return structstore::to_python(*FieldView{t}, recursive);
    }

public:
    template<typename T>
    static void
    register_vector_py(nb::class_<structstore::vector<T>>& cls) {
        // todo: cls.def("lock", ...)
        cls.def("__len__", [](structstore::vector<T>& vec) {
            // todo: lock()
            return vec.size();
        });
        cls.def(
                "insert",
                [](structstore::vector<T>& vec, size_t index, nb::handle& value) {
                    // todo: lock()
                    MiniMalloc& mm_alloc = vec.get_allocator().get_alloc();
                    T& t = *vec.insert(vec.begin() + index, T{});
                    _from_python<T>(t, mm_alloc, value, std::to_string(index));
                },
                nb::arg("index"), nb::arg("value").none());
        cls.def("extend", [](structstore::vector<T>& vec, nb::iterable& value) {
            // todo: lock()
            MiniMalloc& mm_alloc = vec.get_allocator().get_alloc();
            for (const auto& val: value) {
                T& t = vec.emplace_back();
                _from_python<T>(t, mm_alloc, val, std::to_string(vec.size() - 1));
            }
        });
        cls.def(
                "append",
                [](structstore::vector<T>& vec, nb::handle& value) {
                    // todo: lock()
                    std::cout << 1.01 << std::endl;
                    MiniMalloc& mm_alloc = vec.get_allocator().get_alloc();
                    std::cout << "got len " << vec.size() << std::endl;
                    if (vec.size() == 1) {
                        std::cout << "got elem at " << &vec.back() << std::endl;
                    }
                    std::cout << 1.1 << std::endl;
                    vec.reserve(vec.size() + 1);
                    std::cout << 1.15 << std::endl;
                    T& t = vec.emplace_back();
                    std::cout << 1.2 << (&t == &vec.back()) << std::endl;
                    std::cout << 1.3 << std::endl;
                    _from_python<T>(t, mm_alloc, value, std::to_string(vec.size() - 1));
                    std::cout << 1.4 << std::endl;
                },
                nb::arg("value").none());
        cls.def("pop", [](structstore::vector<T>& vec, size_t index) {
            // todo: lock()
            auto ret = _to_python<T>(vec.at(index), true);
            vec.erase(vec.begin() + index);
            return ret;
        });
        //        cls.def("__add__", [](structstore::vector<T>& vec, nb::list&
        //        value) {
        //            // todo: lock()
        //            return to_python(vec, false) + value;
        //        });
        //        cls.def("__iadd__", [](structstore::vector<T>& vec, nb::list&
        //        value) {
        //            // todo: lock()
        //            for (const auto& val: value) {
        //                from_python(vec.push_back(), val,
        //                std::to_string(vec.size() - 1));
        //            }
        //            return to_python(vec, false);
        //        });
        //        cls.def("__setitem__", [](structstore::vector<T>& vec, size_t
        //        index, nb::handle& value) {
        //            // todo: lock()
        //            from_python(vec[index], value, std::to_string(index));
        //        }, nb::arg("index"), nb::arg("value").none());
        //        cls.def("__getitem__", [](structstore::vector<T>& vec, size_t
        //        index) {
        //            // todo: lock()
        //            std::cout << "getting vec item of type " <<
        //            typing::get_type_name(vec[index].get_field().get_type_hash())
        //                      << std::endl;
        //            return to_python(vec[index].get_field(), false);
        //        });
        //        cls.def("__delitem__", [](structstore::vector<T>& vec, size_t
        //        index) {
        //            // todo: lock()
        //            vec.erase(index);
        //        });
        //        cls.def("__iter__", [](structstore::vector<T>& vec) {
        //            // todo: lock()
        //            // todo: use proper type string
        //            return nb::make_iterator(nb::type<structstore::vector<T>>(),
        //            "vec_iter", vec.begin(), vec.end());
        //        }, nb::keep_alive<0, 1>());
        //        cls.def("clear", [](structstore::vector<T>& vec) {
        //            // todo: lock()
        //            vec.clear();
        //        });
    }
};

template<typename T>
nb::class_<T> register_struct_type_and_py(nb::module_& m, const std::string& name) {
    static_assert(std::is_base_of<Struct, T>::value,
                  "template parameter is not derived from structstore::Struct");
    typing::register_type<T>(name);
    typing::register_mm_alloc_constructor<T>();
    typing::register_default_destructor<T>();
    typing::register_default_serializer_text<T>();
    typing::register_check<T>([](MiniMalloc&, const T* t) {
        get_store(*t).check();
    });

    auto nb_cls = nb::class_<T>(m, name.c_str());
    // nb_cls.def(nb::init());
    nb_cls.def("__init__", [=](T* t) { try_with_info("in constructor of " << name << ": ", new (t) T();); });
    py::register_basic_py<T>(nb_cls);
    py::register_structstore_py(nb_cls);
    return nb_cls;
}

} // namespace structstore

#endif
