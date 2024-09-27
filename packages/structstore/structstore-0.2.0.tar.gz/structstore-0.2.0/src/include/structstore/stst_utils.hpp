#ifndef STST_UTILS_HPP
#define STST_UTILS_HPP

#include <sstream>

#define try_with_info(info_stream, stmt)                                     \
    do {                                                                     \
        try {                                                                \
            if (false) std::cout << "checking " << info_stream << std::endl;            \
            stmt                                                             \
        } catch (std::runtime_error & _e) {                                  \
            std::cout << info_stream << "error: " << _e.what() << std::endl; \
            std::ostringstream _str;                                         \
            _str << info_stream << _e.what();                                \
            throw std::runtime_error(_str.str());                            \
        }                                                                    \
        std::cout << info_stream << "success" << std::endl;                  \
    } while (0)

#endif