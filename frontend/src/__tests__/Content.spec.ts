import { render, fireEvent, screen } from '@testing-library/svelte'
import { describe, it, expect, vi } from 'vitest'
import Content from '../Content.svelte'

describe('Content.svelte', () => {
  const articles = [
    { id: 1, title: 'Hello World', readTime: '3 min', commentsCount: 5 }
  ]

  it('renders articles with title and read time', () => {
    render(Content, { props: { articles } })

    expect(screen.getByText('Hello World')).toBeInTheDocument()
    expect(screen.getByText('3 min')).toBeInTheDocument()
  })

  it('shows comment count and fires openSidebar event', async () => {
    const { component } = render(Content, { props: { articles } })
    const openHandler = vi.fn()
    component.$on('openSidebar', openHandler)

    const countEl = screen.getByText('5 comments')
    expect(countEl).toBeInTheDocument()

    await fireEvent.click(countEl)
    expect(openHandler).toHaveBeenCalledWith(
      expect.objectContaining({ detail: 1 })
    )
  })
})
