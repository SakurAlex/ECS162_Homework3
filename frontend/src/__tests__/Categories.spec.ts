// frontend/src/__tests__/Categories.spec.ts
import { render, screen } from '@testing-library/svelte'
import { describe, it, expect } from 'vitest'
import Categories from '../Categories.svelte'

describe('Categories.svelte', () => {
  const sample = ['News', 'Tech', 'Sports']

  it('renders all categories and highlights the active one', () => {
    render(Categories, {
      props: {
        categories: sample,
        activeCategory: 'Tech'
      }
    })

    // every category label shows up…
    sample.forEach((cat) => {
      expect(screen.getByText(cat)).toBeInTheDocument()
    })

    // …and 'Tech' has the active marker
    expect(screen.getByText('Tech')).toHaveClass('active')
  })
})
