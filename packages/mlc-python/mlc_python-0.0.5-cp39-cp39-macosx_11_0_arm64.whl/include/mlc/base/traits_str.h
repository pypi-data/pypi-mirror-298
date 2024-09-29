#ifndef MLC_BASE_TRAITS_STR_H_
#define MLC_BASE_TRAITS_STR_H_

#include "./utils.h"

namespace mlc {
namespace base {

template <> struct PODTraits<const char *> {
  static constexpr int32_t default_type_index = static_cast<int32_t>(MLCTypeIndex::kMLCRawStr);
  static void TypeCopyToAny(const char *src, MLCAny *ret) {
    ret->type_index = static_cast<int32_t>(MLCTypeIndex::kMLCRawStr);
    ret->v_str = src;
  }
  static const char *AnyCopyToType(const MLCAny *v) {
    MLCTypeIndex type_index = static_cast<MLCTypeIndex>(v->type_index);
    if (type_index == MLCTypeIndex::kMLCRawStr) {
      return v->v_str;
    }
    if (type_index == MLCTypeIndex::kMLCStr) {
      return reinterpret_cast<MLCStr *>(v->v_obj)->data;
    }
    throw TemporaryTypeError();
  }
  static const char *Type2Str() { return "const char *"; }
  static std::string __str__(const char *src) { return '"' + std::string(src) + '"'; }
};

template <> struct PODTraits<char *> {
  static constexpr int32_t default_type_index = static_cast<int32_t>(MLCTypeIndex::kMLCRawStr);
  static void TypeCopyToAny(char *src, MLCAny *ret) { return PODTraits<const char *>::TypeCopyToAny(src, ret); }
  static char *AnyCopyToType(const MLCAny *v) { return const_cast<char *>(PODTraits<const char *>::AnyCopyToType(v)); }
  static const char *Type2Str() { return "const char *"; }
  static std::string __str__(const char *src) { return '"' + std::string(src) + '"'; }
};

template <> struct PODTraits<std::string> {
  static constexpr int32_t default_type_index = static_cast<int32_t>(MLCTypeIndex::kMLCRawStr);
  static void TypeCopyToAny(const std::string &src, MLCAny *ret) {
    return PODTraits<const char *>::TypeCopyToAny(src.data(), ret);
  }
  static std::string AnyCopyToType(const MLCAny *v) { return PODTraits<const char *>::AnyCopyToType(v); }
  static const char *Type2Str() { return "str"; }
  static std::string __str__(const char *src) { return '"' + std::string(src) + '"'; }
};

template <size_t N> struct PODTraits<char[N]> : public PODTraits<const char *> {};

} // namespace base
} // namespace mlc

#endif // MLC_BASE_TRAITS_STR_H_
