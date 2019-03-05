///
/// \file List.h
/// \copyright Festo AG & Co. KG, Esslingen. All rights reserved.
/// \author hpw (Owner)
/// $Revision: $
/// \brief Class for list-functionality

#pragma once

#include "FMCTypes.h"

namespace Utilities
{

/// Template for a generic list of constant size to add, insert and remove elements with linear
/// complexity.
/// \details A simple example:
/// \code
///   Basics::List<int, 3ul> list; // A list of type int with a maximum of three elements.
///   list.add(3);                 // Add elements to list.
///   list.add(5);
/// \endcode
/// \tparam T Type name of elements to store.
/// \tparam maxSize Maximum number of elements to store.
template <typename T, UINT32 maxSize>
class List
{
public:
    /// Construct an empty list.
    List()
    {
        count = 0;
    }


    /// Clear all elements from the list.
    inline void clear()
    {
        count = 0;
    }

    /// Obtain the maximum number of elements to store.
    /// \returns Maximum number of elements to store.
    inline UINT32 getMaxSize() const
    {
        return maxSize;
    }

    /// Obtain number of elements currently stored.
    /// \returns Number of elements currently stored.
    inline UINT32 getCount() const
    {
        return count;
    }

    /// Check whether the list is completely filled with elements.
    /// \returns #true in case the list completely filled or #false otherwise. Addition and
    /// insertion of elements is not possible if the list is completely filled.
    inline BOOL isFull() const
    {
        return(count >= maxSize);
    }

    /// Check whether the list stores no elements.
    /// \returns #true if the number of elements currently stored in the list is empty or #false
    /// otherwise.
    /// \note If the maximum size of the list is zero, it returns #true although no elements can be
    /// stored.
    inline BOOL isEmpty() const
    {
        return(count == 0);
    }

    /// Return element at given position.
    /// \param[in] _pos Position of the element to return.
    /// \returns Element of the list at position \p _pos.
    /// \warning The return value is undefined unless 0 <= \p _pos < #getCount.
    inline T& operator[](const UINT32 _pos)
    {
        return arr[_pos];
    }

    /// Return element at given position.
    /// \param[in] _pos Position of the element to return.
    /// \returns Element of the list at position \p _pos.
    /// \warning The return value is undefined unless 0 <= \p _pos < #getCount.
    inline const T& operator[](const UINT32 _pos) const
    {
        return arr[_pos];
    }

    /// Add element at the end in constant time O(1).
    /// \param[in] _value Element to add.
    /// \returns Position of the element added if the list is not full (see #isFull) or
    /// the maximum number of elements (see #getMaxSize) otherwise.
    UINT32 add(const T& _value)
    {
        UINT32 result = maxSize;
        if (count < maxSize)
        {
            // Assign value and increment count
            arr[count] = _value;
            result = count;
            count++;
        }
        return result;
    }

    /// Insert element at a given position in linear time O(n).
    /// \details The elements located after the specified position are shifted downwards and the
    /// number of the list is increased by one. Thus the operations takes place in linear time O(n).
    /// \param[in] _pos Position in the list to insert the item at. Use zero to insert the element at
    /// the very first or #getCount to add it at the end. The latter is similar to (#add). If
    /// \p _pos is greater or equal than #getCount, the item will always be added at the end
    /// (independent of whether \p _pos is actual a valid position).
    /// \param[in] _value Element to insert.
    /// \returns Position of the element added if the list is not full (see #isFull) or
    /// the maximum number of elements (see #getMaxSize) otherwise.
    UINT32 insert(const UINT32 _pos, const T& _value)
    {
        UINT32 result = maxSize;
        if (count < maxSize)
        {
            // Check whether the item shall be added at the end.
            if (_pos >= count)
            {
                result = add(_value);
            }
            else
            {
                // Shift elements by one position upwards
                for (UINT32 i = count; i > _pos; i--)
                {
                    arr[i] = arr[i - 1];
                }
                arr[_pos] = _value;
                result = _pos;
                count++;
            }
        }
        return result;
    }

    /// Remove element at a given position.
    /// \details The elements located after the specified position are shifted upwards and the
    /// number of the list is decreased by one. Thus the operations takes place in linear time O(n).
    /// \param[in] _pos Position of the element to remove. Use zero to remove the first element or
    /// (#getCount - 1) to remove the last.
    /// \returns #true if an element at the given position was found and removed or #false
    /// otherwise.
    BOOL remove(const UINT32 _pos)
    {
        BOOL result = false;
        if (maxSize > 1)
        {
            if (_pos < count && count <= maxSize)
            {
                // Shift elements by one position upwards
                for (UINT32 i = _pos; i < (count - 1); i++)
                {
                    arr[i] = arr[i + 1];
                }
                // Decrement count
                count--;
                result = true;
            }
        }
        else
        {
            // There is only one element that can be removed
            if ((_pos == 0) && (count == 1))
            {
                count = 0;
                result = true;
            }
        }
        return result;
    }

    /// Template callback function for method #removeIf.
    /// \param[in] _value Elements to match.
    /// \returns The return value is given by the callee and depends on the context in which the
    /// callback is called in. See #removeIf for context.
    typedef BOOL matchCallback(T& _value, void* ptr);

    /// Remove element(s) from the list that match a certain callback.
    /// \details Removing elements one by one from a list is rather slow, since for every #remove
    /// the elements have to be shifted upwards. Thus this algorithm loops through the list and
    /// removes the elements that match \p _callback in linear time O(n). For elements to be removed
    /// the callee needs to return #true. For #false the elements are kept.
    /// \param[in] _callback Callback method to match elements to remove.
    /// \param[in] _ptr Additional data to pass to the callback method.
    /// \returns The number of elements removed.
    UINT32 removeIf(matchCallback& _callback, void* _ptr = NULL)
    {
        UINT32 countOfRemoved = 0;
        for (UINT32 i = 0; i < count; i++)
        {
            if (_callback(arr[i], _ptr) == true)
            {
                countOfRemoved++;
            }
            else
            {
                // Shift elements upwards by the number of elements removed before.
                arr[i - countOfRemoved] = arr[i];
            }
        }
        // Decrease size of the list at the end.
        count -= countOfRemoved;
        return countOfRemoved;
    }

    /// Obtain index of element in list in linear time O(n).
    /// \param[in] _value Element to find.
    /// \returns Position of the element added if the list is not full (see #isFull) or
    /// the maximum number of elements (see #getMaxSize) otherwise.
    UINT32 find(const T& _value) const
    {
        for (UINT32 i = 0; i < getCount(); i++)
        {
            if (arr[i] == _value)
            {
                return(i);
            }
        }
        return(maxSize);
    }

protected:
    /// Storage for the list
    T arr[maxSize];
    /// Number of elements in the list
    UINT32 count;
};

}// namespace utilities
