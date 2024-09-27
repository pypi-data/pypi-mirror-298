#ifndef STST_LOCK_HPP
#define STST_LOCK_HPP

#include <unistd.h>

#include <atomic>
#include <iostream>

namespace structstore {

class SpinMutex {
    std::atomic_int flag{0};
    int lock_level = 0;

    // too many keywords
    inline static thread_local const int tid = gettid();

public:

    SpinMutex() = default;

    SpinMutex(SpinMutex&&) = delete;

    SpinMutex(const SpinMutex&) = delete;

    SpinMutex& operator=(SpinMutex&&) = delete;

    SpinMutex& operator=(const SpinMutex&) = delete;

    void lock() {
//        std::cout << "locking " << this << std::endl;
        int v = flag.load(std::memory_order_relaxed);
        if (v == tid) {
            ++lock_level;
//            std::cout << "already locked " << this << " at level " << lock_level << std::endl;
            return;
        }
        v = 0;
        while (!flag.compare_exchange_strong(v, tid, std::memory_order_acquire)) {
            while ((v = flag.load(std::memory_order_relaxed)) != 0) { }
        }
        ++lock_level;
//        std::cout << "got lock at " << this << " at level " << lock_level << std::endl;
    }

    void unlock() {
        if ((--lock_level) == 0) {
//            std::cout << "completely unlocked " << this << std::endl;
            flag.store(0, std::memory_order_release);
        }
//        std::cout << "unlocking " << this << " to level " << lock_level << std::endl;
    }
};

class ScopedLock {
    SpinMutex* mutex = nullptr;

    ScopedLock() : mutex{nullptr} {}

public:
    explicit ScopedLock(SpinMutex& mutex) : mutex(&mutex) {
        mutex.lock();
    }

    void unlock() {
        if (mutex) {
            mutex->unlock();
            mutex = nullptr;
        }
    }

    ~ScopedLock() {
        unlock();
    }

    ScopedLock(ScopedLock&& other) noexcept: ScopedLock() {
        *this = std::move(other);
    }

    ScopedLock& operator=(ScopedLock&& other) noexcept {
        std::swap(mutex, other.mutex);
        return *this;
    }

    ScopedLock(const ScopedLock&) = delete;

    ScopedLock& operator=(const ScopedLock&) = delete;
};

}

#endif
