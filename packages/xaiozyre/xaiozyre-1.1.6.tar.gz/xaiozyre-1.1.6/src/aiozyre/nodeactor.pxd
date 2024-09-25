# cython: language_level=3

from . cimport zyre as z


cdef class NodeActor:
    cdef public str uuid
    cdef public object started
    cdef public object stopped
    cdef public object config
    cdef public object loop
    cdef public object inbox
    cdef public object outbox

    # private
    cdef z.zyre_t * zyre
    cdef z.zpoller_t * zpoller
    cdef z.zactor_t * zactor
    cdef z.zsock_t * zactor_pipe
    cdef unsigned long zthreadid
    cdef unsigned long lthreadid


cdef void node_act(z.zsock_t * pipe, void * _actor) noexcept nogil
