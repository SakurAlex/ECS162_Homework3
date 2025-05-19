import { describe, it, expect, vi, beforeEach } from 'vitest'
import {
  fetchArticles,
  fetchComments,
  postComment,
  deleteComment,
} from '../lib/api'

describe('api.ts', () => {
  beforeEach(() => {
    global.fetch = vi.fn()
  })

  it('fetchArticles calls correct URL and returns JSON', async () => {
    const mock = { response: { docs: [1,2] } }
    ;(global.fetch as any).mockResolvedValue({ json: () => Promise.resolve(mock) })

    const result = await fetchArticles()
    expect(global.fetch).toHaveBeenCalledWith(
      `${import.meta.env.VITE_BASE_URL || ''}/api/ucdavis-news`,
      { credentials: 'include' }
    )
    expect(result).toEqual(mock)
  })

  it('fetchComments calls with article_id', async () => {
    const mock = ['a','b']
    ;(global.fetch as any).mockResolvedValue({ json: () => Promise.resolve(mock) })

    const data = await fetchComments('XYZ')
    expect(global.fetch).toHaveBeenCalledWith(
      `${import.meta.env.VITE_BASE_URL || ''}/api/comments?article_id=XYZ`,
      { credentials: 'include' }
    )
    expect(data).toEqual(mock)
  })

  it('postComment and deleteComment use correct methods', async () => {
    ;(global.fetch as any).mockResolvedValue({ json: () => Promise.resolve({ ok: true }) })

    await postComment('A1','hello')
    expect(global.fetch).toHaveBeenLastCalledWith(
      `${import.meta.env.VITE_BASE_URL || ''}/api/comments`,
      expect.objectContaining({ method: 'POST' })
    )

    await deleteComment('CID123')
    expect(global.fetch).toHaveBeenLastCalledWith(
      `${import.meta.env.VITE_BASE_URL || ''}/api/comments/CID123`,
      expect.objectContaining({ method: 'DELETE' })
    )
  })
})
